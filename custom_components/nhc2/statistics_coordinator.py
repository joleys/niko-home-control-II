"""Coordinator for fetching and importing measurement statistics."""
import logging
from datetime import datetime, timedelta, timezone

from homeassistant.core import HomeAssistant
from homeassistant.components.recorder import get_instance
from homeassistant.components.recorder.statistics import (
    async_add_external_statistics,
    get_last_statistics,
    StatisticData,
    StatisticMetaData,
    StatisticMeanType,
)
from homeassistant.const import UnitOfEnergy, UnitOfVolume

from .nhccoco.coco import CoCo
from .nhccoco.measurements_client import MeasurementsClient
from .nhccoco.devices.device import CoCoDevice
from .const import (
    DOMAIN,
    MEASUREMENT_PROPERTIES_FILTER,
    MEASUREMENT_HISTORY_DAYS,
    CONF_ENABLE_STATISTICS,
    CONF_IMPORT_HISTORICAL_STATISTICS,
    CONF_HISTORICAL_STATISTICS_IMPORTED,
)

_LOGGER = logging.getLogger(__name__)

TWO_MONTHS_DAYS = 60
MAX_HOURLY_INTERVAL_DAYS = 63  # API limitation for hourly aggregated data
MAX_DAILY_INTERVAL_DAYS = 100  # API limitation for daily aggregated data


def align_to_hour(dt: datetime) -> datetime:
    aligned = dt.replace(minute=0, second=0, microsecond=0)
    
    # Ensure timezone info is present (assume UTC if missing)
    if aligned.tzinfo is None:
        aligned = aligned.replace(tzinfo=timezone.utc)
    
    return aligned

def align_to_midnight(dt: datetime) -> datetime:
    aligned = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Ensure timezone info is present (assume UTC if missing)
    if aligned.tzinfo is None:
        aligned = aligned.replace(tzinfo=timezone.utc)
    
    return aligned

class StatisticsCoordinator:
    def __init__(
        self,
        hass: HomeAssistant,
        gateway: CoCo,
        measurements_client: MeasurementsClient,
        config_entry,
    ):
        self._hass = hass
        self._gateway = gateway
        self._measurements_client = measurements_client
        self._config_entry = config_entry

    async def async_setup(self):
        # Check if statistics are enabled
        if not self._config_entry.options.get(CONF_ENABLE_STATISTICS, False):
            _LOGGER.info("Statistics are disabled, skipping statistics setup")
            return

        _LOGGER.info("Setting up statistics coordinator")

        # Check if we should import historical data and it hasn't been done yet
        should_import_historical = self._config_entry.options.get(CONF_IMPORT_HISTORICAL_STATISTICS, False)
        historical_imported = self._config_entry.options.get(CONF_HISTORICAL_STATISTICS_IMPORTED, False)
        
        if should_import_historical and not historical_imported:
            _LOGGER.info("Importing long term energy data (one-time operation)")
            await self.async_import_longterm_data()

            # Mark historical data as imported
            self._hass.config_entries.async_update_entry(
                self._config_entry,
                options={
                    **self._config_entry.options,
                    CONF_HISTORICAL_STATISTICS_IMPORTED: True
                }
            )
            _LOGGER.info("Historical data import completed and marked as done")

        _LOGGER.info("Importing recent data")
        await self.async_import_recent_data()

    def _get_devices_with_measurements(self):
        for device in self._gateway._device_instances.values():
            if isinstance(device, CoCoDevice):
                measurement_properties = device.get_measurement_properties(MEASUREMENT_PROPERTIES_FILTER)
                if measurement_properties:
                    yield device, measurement_properties

    async def _async_import_data(self, longterm: bool = False):
        devices_with_measurements = list(self._get_devices_with_measurements())
        _LOGGER.debug(f"Found {len(devices_with_measurements)} devices with measurement properties")
        for device, measurement_properties in devices_with_measurements:
            _LOGGER.debug(
                f"Device {device.name} ({device.uuid}) has following measurement properties: "
                f"{measurement_properties}"
            )
            for property_name in measurement_properties:
                await self._import_property_data(device, property_name, longterm=longterm)

    async def async_import_longterm_data(self):
        _LOGGER.info("Starting long term historical data import (data older than 2 months up to 10 years back)")
        await self._async_import_data(longterm=True)

    async def async_import_recent_data(self):
        _LOGGER.info("Starting recent data import (last 2 months)")
        await self._async_import_data(longterm=False)

    def _generate_statistic_id(self, device: CoCoDevice, property_name: str) -> str:
        safe_uuid = device.uuid.replace('-', '_').lower()
        return f"{DOMAIN}:{safe_uuid}_{property_name.lower()}"

    def _calculate_time_range(
        self, statistic_id: str, last_stats: dict, longterm: bool
    ) -> tuple[datetime, datetime] | None:
        two_months_ago = datetime.now(timezone.utc) - timedelta(days=TWO_MONTHS_DAYS)
        two_months_ago = align_to_midnight(two_months_ago)
        
        if longterm:
            # Import only data older than 2 months up to 10 years back
            start_time = datetime.now(timezone.utc) - timedelta(days=MEASUREMENT_HISTORY_DAYS)
            end_time = two_months_ago
            start_time = align_to_midnight(start_time)
            end_time = align_to_midnight(end_time)
            _LOGGER.info(f"Importing long term historical data from {start_time} to {end_time}")
        else:
            end_time = align_to_hour(datetime.now(timezone.utc))

            if statistic_id in last_stats and last_stats[statistic_id]:
                # We have existing data, only fetch new data since last data point
                last_stat_start_time_utc = datetime.fromtimestamp(
                    last_stats[statistic_id][0]["start"], tz=timezone.utc
                )
                last_stat_end_time_utc = last_stat_start_time_utc + timedelta(hours=1)
                _LOGGER.debug(f"Last statistic for {statistic_id} runs until {last_stat_end_time_utc}")
                start_time = max(last_stat_end_time_utc, two_months_ago)
            else:
                # No existing data, fetch from 2 months ago
                start_time = two_months_ago
                _LOGGER.debug(f"No existing statistics for {statistic_id}, importing all hourlies from 2 months ago")

            start_time = align_to_hour(start_time)

        # Skip if start_time is after or equal to end_time
        if start_time >= end_time:
            _LOGGER.info(f"No new data to import for {statistic_id}")
            return None

        if not longterm:
            start_time = start_time + timedelta(hours=1)
            end_time = end_time + timedelta(hours=1)
    
        _LOGGER.debug(f"Importing data from {start_time} to {end_time} for {statistic_id}")
        return start_time, end_time

    def _process_api_values(self, values: list, adjust_hour: bool = False) -> list[dict]:
        statistics_data = []
        for value in values:
            if "DateTime" in value and "Value" in value and value["Value"] is not None:
                dt = datetime.fromisoformat(value["DateTime"])
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if adjust_hour:
                    dt = dt - timedelta(hours=1)
                statistics_data.append({"start": dt, "value": value["Value"]})
        return statistics_data

    async def _fetch_aggregated_data(
        self,
        device: CoCoDevice,
        property_name: str,
        start_time: datetime,
        end_time: datetime,
        period: str,
        max_days: int,
        adjust_hour: bool = False
    ) -> list[dict]:
        _LOGGER.info(f"Fetching {period} aggregated data from {start_time} to {end_time}")
        statistics_data = []

        current_start = start_time
        while current_start < end_time:
            chunk_end = min(current_start + timedelta(days=max_days), end_time)
            _LOGGER.debug(f"Fetching {period} chunk from {current_start} to {chunk_end}")

            data = await self._measurements_client.get_aggregated_measurements(
                device.uuid, property_name, period, current_start, chunk_end, "sum"
            )
            
            if data and "Values" in data:
                statistics_data.extend(self._process_api_values(data["Values"], adjust_hour))
            
            current_start = chunk_end
            
        _LOGGER.debug(f"Retrieved {len(statistics_data)} {period} data points")
        return statistics_data

    async def _fetch_daily_data(
        self, device: CoCoDevice, property_name: str, start_time: datetime, end_time: datetime
    ) -> list[dict]:
        return await self._fetch_aggregated_data(
            device, property_name, start_time, end_time, "day", MAX_DAILY_INTERVAL_DAYS
        )

    async def _fetch_hourly_data(
        self, device: CoCoDevice, property_name: str, start_time: datetime, end_time: datetime
    ) -> list[dict]:
        return await self._fetch_aggregated_data(
            device, property_name, start_time, end_time, "hour", MAX_HOURLY_INTERVAL_DAYS, adjust_hour=True
        )

    def _build_statistic_entries(self, statistics_data: list[dict], initial_sum: float) -> list[StatisticData]:
        statistics_data.sort(key=lambda x: x["start"])
        statistic_entries = []
        cumulative_sum = initial_sum

        for data_point in statistics_data:
            cumulative_sum += data_point["value"]
            statistic_entries.append(
                StatisticData(start=data_point["start"], state=data_point["value"], sum=cumulative_sum)
            )

        return statistic_entries

    def _get_currency_symbol(self) -> str:
        # Try to get currency from Home Assistant configuration
        if hasattr(self._hass.config, 'currency') and self._hass.config.currency:
            _LOGGER.debug(f"Using currency from Home Assistant config: {self._hass.config.currency}")
            return self._hass.config.currency
        _LOGGER.debug("No currency configured in Home Assistant, defaulting to EUR")
        # Default to EUR (Euro currency code)
        return "EUR"

    def _create_metadata(self, device: CoCoDevice, property_name: str, statistic_id: str) -> StatisticMetaData:
        if "Cost" in property_name:
            unit = self._get_currency_symbol()
            unit_class = None
        elif "ElectricalEnergy" in property_name:
            unit = UnitOfEnergy.WATT_HOUR
            unit_class = "energy"
        elif "WaterVolume" in property_name:
            unit = UnitOfVolume.LITERS
            unit_class = "volume"
        elif "GasVolume" in property_name:
            unit = UnitOfVolume.CUBIC_METERS
            unit_class = "volume"
        else:
            unit = None
            unit_class = None

        return StatisticMetaData(
            has_mean=False,
            has_sum=True,
            name=f"{device.name} {property_name}",
            source=DOMAIN,
            statistic_id=statistic_id,
            unit_of_measurement=unit,
            unit_class=unit_class,
            mean_type=StatisticMeanType.NONE,
        )

    async def _import_property_data(
        self, device: CoCoDevice, property_name: str, longterm: bool = False
    ):
        statistic_id = self._generate_statistic_id(device, property_name)
        _LOGGER.debug(f"Importing data for {statistic_id} (longterm={longterm})")
        
        last_stats = await get_instance(self._hass).async_add_executor_job(
            get_last_statistics, self._hass, 1, statistic_id, True, {"sum"}
        )

        time_range = self._calculate_time_range(statistic_id, last_stats, longterm)
        if time_range is None:
            return

        start_time, end_time = time_range

        if longterm:
            statistics_data = await self._fetch_daily_data(device, property_name, start_time, end_time)
        else:
            statistics_data = await self._fetch_hourly_data(device, property_name, start_time, end_time)

        if not statistics_data:
            _LOGGER.warning(f"No measurement data retrieved for {statistic_id}")
            return

        initial_sum = 0
        if statistic_id in last_stats and last_stats[statistic_id]:
            sum_value = last_stats[statistic_id][0]["sum"]
            initial_sum = sum_value if sum_value is not None else 0

        statistic_entries = self._build_statistic_entries(statistics_data, initial_sum)
        
        if not statistic_entries:
            _LOGGER.info(f"No valid statistics to import for {statistic_id}")
            return

        metadata = self._create_metadata(device, property_name, statistic_id)
        async_add_external_statistics(self._hass, metadata, statistic_entries)

        _LOGGER.debug(f"Imported {len(statistic_entries)} statistics for {statistic_id}")

    async def async_shutdown(self):
        _LOGGER.info("Shutting down statistics coordinator")
        await self._measurements_client.close()
