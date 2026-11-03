from datetime import datetime, time, timedelta

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.util import dt as dt_util

from ..nhccoco.devices.generic_chargingstation import CocoGenericChargingstation
from .nhc_entity import NHCBaseEntity


def next_charging_timestamp(charging_time: time, now: datetime) -> datetime:
    """Compute the next absolute occurrence of a time of day.

    The controller only reports a time of day (HH:MM), so when the time
    is no longer in the future today, it is assumed to be tomorrow.
    """
    candidate = now.replace(
        hour=charging_time.hour,
        minute=charging_time.minute,
        second=0,
        microsecond=0,
    )
    return candidate if candidate > now else candidate + timedelta(days=1)


class Nhc2GenericChargingstationNextChargingTimeEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericChargingstation, hub, gateway):
        """Initialize the next charging time entity."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_next_charging_time'
        self._attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def name(self) -> str:
        return 'Next Charging Time'

    @property
    def state(self) -> datetime | None:
        """Return the next charging start as an absolute timestamp.

        A timestamp sensor requires a full date and time. The controller
        only sends a time of day, so the next occurrence is used. Without
        this, the frontend cannot parse the value and shows
        'Invalid timestamp'.
        """
        charging_time = self._device.next_charging_time
        if charging_time is None:
            return None
        return next_charging_timestamp(charging_time, dt_util.now())