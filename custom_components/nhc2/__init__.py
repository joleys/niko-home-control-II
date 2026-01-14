"""Support for Niko Home Control II - CoCo."""
import logging
import ssl
from pathlib import Path

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_PORT, \
    EVENT_HOMEASSISTANT_STOP
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry, issue_registry, entity_registry as er
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval, async_track_time_change

from datetime import timedelta

from .config_flow import Nhc2FlowHandler  # noqa  pylint_disable=unused-import
from .const import (
    DEFAULT_USERNAME,
    DOMAIN,
    KEY_GATEWAY,
    KEY_TOKEN_TIMER_CANCEL,
    KEY_STATISTICS_TIMER_CANCEL,
    KEY_MEASUREMENTS_CLIENT,
    KEY_STATISTICS_COORDINATOR,
    BRAND,
    CONF_ENABLE_STATISTICS,
)
from .nhccoco.helpers import extract_versions
from .nhccoco.const import MQTT_RC_CODES
from .nhccoco.coco import CoCo
from .nhccoco.measurements_client import MeasurementsClient
from .statistics_coordinator import StatisticsCoordinator
from .hobbytoken import HobbyToken

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_PORT): vol.All(vol.Coerce(int), vol.Range(min=0, max=65535))
    })
}, extra=vol.ALLOW_EXTRA)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate old config entries to the latest version.

    Version 1 → 2: update unique_id for controller update entity to be per-host,
    preventing duplicate IDs when multiple controllers are configured.
    """

    if entry.version is None or entry.version < 2:
        registry = er.async_get(hass)
        old_unique_id = "controller_has_newer_config"
        new_unique_id = f"{entry.data.get(CONF_HOST)}_controller_has_newer_config"

        # Update any existing entity registry entries using the old unique_id
        for entity_entry in list(registry.entities.values()):
            if (
                entity_entry.config_entry_id == entry.entry_id
                and entity_entry.domain == "update"
                and entity_entry.platform == DOMAIN
                and entity_entry.unique_id == old_unique_id
            ):
                registry.async_update_entity(entity_entry.entity_id, new_unique_id=new_unique_id)

        hass.config_entries.async_update_entry(entry, version=2)
        _LOGGER.debug(
            "Migrated nhc2 config entry %s to version %s (update unique_id %s)",
            entry.entry_id,
            2,
            new_unique_id,
        )

    return True


async def async_setup(hass, config):
    """Set up the NHC2 CoCo component."""
    conf = config.get(DOMAIN)

    if conf is None:
        return True

    host = conf.get(CONF_HOST)
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)
    port = conf.get(CONF_PORT)

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={'source': config_entries.SOURCE_IMPORT},
            data={
                CONF_HOST: host,
                CONF_USERNAME: username,
                CONF_PASSWORD: password,
                CONF_PORT: port
            }
        )
    )

    return True


FORWARD_PLATFORMS = (
    "alarm_control_panel",
    "binary_sensor",
    "button",
    "camera",
    "climate",
    "cover",
    "fan",
    "light",
    "lock",
    "media_player",
    "number",
    "select",
    "sensor",
    "switch",
    "time",
    "update",
)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    for platform in FORWARD_PLATFORMS:
        hass.add_job(
            hass.config_entries.async_forward_entry_unload(entry, platform)
        )
    coco: CoCo = hass.data[KEY_GATEWAY][entry.entry_id]
    if coco:
        coco.disconnect()
    
    # Shutdown statistics coordinator if it exists
    if KEY_STATISTICS_COORDINATOR in hass.data and entry.entry_id in hass.data[KEY_STATISTICS_COORDINATOR]:
        coordinator: StatisticsCoordinator = hass.data[KEY_STATISTICS_COORDINATOR][entry.entry_id]
        await coordinator.async_shutdown()
    
    # Close measurements client if it exists
    if KEY_MEASUREMENTS_CLIENT in hass.data and entry.entry_id in hass.data[KEY_MEASUREMENTS_CLIENT]:
        client: MeasurementsClient = hass.data[KEY_MEASUREMENTS_CLIENT][entry.entry_id]
        await client.close()
    
    if entry.entry_id in hass.data.get(KEY_TOKEN_TIMER_CANCEL, {}):
        existing_cancel = hass.data[KEY_TOKEN_TIMER_CANCEL][entry.entry_id]
        if existing_cancel:
            existing_cancel()
            hass.data[KEY_TOKEN_TIMER_CANCEL][entry.entry_id] = None

    if entry.entry_id in hass.data.get(KEY_STATISTICS_TIMER_CANCEL, {}):
        existing_cancel = hass.data[KEY_STATISTICS_TIMER_CANCEL][entry.entry_id]
        if existing_cancel:
            existing_cancel()
            hass.data[KEY_STATISTICS_TIMER_CANCEL][entry.entry_id] = None

    return True

async def async_setup_entry(hass, entry):
    token_timer_cancel = None
    if entry.data[CONF_USERNAME] != DEFAULT_USERNAME:
        issue_registry.async_create_issue(
                    hass,
                    DOMAIN,
                    "migrate_to_token_auth",
                    is_fixable=True,
                    severity=issue_registry.IssueSeverity.WARNING,
                    translation_key="migrate_to_token_auth",
                    data={'entry': entry}
            )
    else:
        token = HobbyToken(entry.data[CONF_PASSWORD])
        def check_token_expiration(timestamp):
            _LOGGER.info("Token is valid until %s", token.get_expiration_date())
            if token.will_expire_soon():
                issue_registry.create_issue(
                        hass,
                        DOMAIN,
                        "token_about_to_expire",
                        is_fixable=True,
                        severity=issue_registry.IssueSeverity.WARNING,
                        translation_key="token_about_to_expire",
                        data={'entry': entry}
                )

        token_timer_cancel = async_track_time_interval(hass, check_token_expiration, timedelta(days=1), cancel_on_shutdown=True)

    """Create an NHC2 gateway."""
    coco = CoCo(
        address=entry.data[CONF_HOST],
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        port=entry.data[CONF_PORT] if CONF_PORT in entry.data else 8884
    )

    async def on_hass_stop(event):
        """Close connection when hass stops."""
        coco.disconnect()

    def process_sysinfo(dev_reg):
        def do_process_sysinfo(nhc2_sysinfo):
            coco_image, nhc_version = extract_versions(nhc2_sysinfo)
            _LOGGER.debug('systeminfo.published: NhcVersion: %s - CocoImage %s', nhc_version, coco_image)

            async def get_or_create_device():
                return dev_reg.async_get_or_create(
                    config_entry_id=entry.entry_id,
                    connections=set(),
                    identifiers={
                        (DOMAIN, entry.data[CONF_USERNAME])
                    },
                    manufacturer=BRAND,
                    name='Home Control II',
                    model='Connected controller',
                    sw_version=nhc_version + ' - CoCo Image: ' + coco_image,
                )

            hass.add_job(get_or_create_device())

        return do_process_sysinfo

    def reload_entities():
        def do_reload_entities():
            if coco.entries_initialized:
                for platform in FORWARD_PLATFORMS:
                    hass.add_job(
                        hass.config_entries.async_forward_entry_unload(entry, platform)
                    )

            hass.add_job(
                hass.config_entries.async_forward_entry_setups(entry, FORWARD_PLATFORMS)
            )

        return do_reload_entities

    def on_connection_refused(connection_result):
        # Possible values for connection_result:
        # 1: Connection refused - incorrect protocol version
        # 2: Connection refused - invalid client identifier
        # 3: Connection refused - server unavailable
        # 4: Connection refused - bad username or password
        # 5: Connection refused - not authorised

        _LOGGER.error(MQTT_RC_CODES[connection_result])

        if connection_result in (4, 5):
            coco.disconnect()
            issue_registry.create_issue(
                hass,
                DOMAIN,
                "not_authorised",
                is_fixable=True,
                severity=issue_registry.IssueSeverity.CRITICAL,
                translation_key="not_authorised",
                data={'entry': entry}
            )

    hass.data.setdefault(KEY_GATEWAY, {})[entry.entry_id] = coco
    hass.data.setdefault(KEY_TOKEN_TIMER_CANCEL, {})[entry.entry_id] = token_timer_cancel 
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)

    # Create SSL context for REST API (done outside event loop to avoid blocking I/O)
    async def create_ssl_context():
        """Create SSL context with certificate in executor."""
        def _load_ssl_context():
            cert_path = Path(__file__).parent / 'nhccoco' / 'coco_ca.pem'
            ssl_context = ssl.create_default_context(cafile=str(cert_path))
            ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
            # Disable hostname checking since we're connecting to an IP address
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            return ssl_context
        
        return await hass.async_add_executor_job(_load_ssl_context)
    
    ssl_context = await create_ssl_context()

    # Initialize measurements client for REST API access
    measurements_client = MeasurementsClient(
        host=entry.data[CONF_HOST],
        token=entry.data[CONF_PASSWORD],  # Using the password/token for authentication
        port=443,
        ssl_context=ssl_context
    )
    hass.data.setdefault(KEY_MEASUREMENTS_CLIENT, {})[entry.entry_id] = measurements_client

    # Initialize statistics coordinator for fetching and importing measurements
    statistics_coordinator = StatisticsCoordinator(
        hass=hass,
        gateway=coco,
        measurements_client=measurements_client,
        config_entry=entry
    )
    hass.data.setdefault(KEY_STATISTICS_COORDINATOR, {})[entry.entry_id] = statistics_coordinator

    dev_reg = device_registry.async_get(hass)
    coco.set_systeminfo_callback(process_sysinfo(dev_reg))
    
    # Setup devices list callback that also triggers statistics import
    def devices_list_callback_with_stats():
        """Callback when devices list is loaded."""
        reload_entities()()
        
        # After devices are loaded, start importing statistics
        # Do this in the background to not block device initialization
        async def start_statistics_import():
            await statistics_coordinator.async_setup()
            
        hass.create_task(start_statistics_import())
    
    coco.set_devices_list_callback(devices_list_callback_with_stats)

    _LOGGER.debug('Connecting to %s', entry.data[CONF_HOST])
    coco.connect(on_connection_refused)

    # Schedule periodic statistics updates at 2 minutes past each hour
    # Only if statistics are enabled
    if entry.options.get(CONF_ENABLE_STATISTICS, False):
        async def update_statistics_periodically(now):
            """Periodic task to update statistics."""
            await statistics_coordinator.async_import_recent_data()

        # Cancel any existing statistics timer before starting a new one
        if entry.entry_id in hass.data.get(KEY_STATISTICS_TIMER_CANCEL, {}):
            existing_cancel = hass.data[KEY_STATISTICS_TIMER_CANCEL][entry.entry_id]
            if existing_cancel:
                existing_cancel()

        statistics_timer_cancel = async_track_time_change(
            hass,
            update_statistics_periodically,
            hour=None,  # Every hour
            minute=2,   # At 2 minutes past the hour
            second=0
        )
        hass.data.setdefault(KEY_STATISTICS_TIMER_CANCEL, {})[entry.entry_id] = statistics_timer_cancel
    else:
        _LOGGER.debug("Periodic statistics updates disabled")
    
    # Listen for options updates
    entry.async_on_unload(entry.add_update_listener(async_options_updated))
    
    # Register service for manual statistics import
    async def handle_import_statistics(call):
        """Handle the import_statistics service call."""
        coordinator = hass.data[KEY_STATISTICS_COORDINATOR][entry.entry_id]
        if coordinator:
            import_type = call.data.get("import_type", "recent")
            
            if import_type in ["both", "longterm"]:
                await coordinator.async_import_longterm_data()
                _LOGGER.info("Long term statistics import completed")
            
            if import_type in ["both", "recent"]:
                await coordinator.async_import_recent_data()
                _LOGGER.info("Recent statistics update completed")
                
            _LOGGER.info("Manual statistics import completed (type: %s)", import_type)
        else:
            _LOGGER.error("Statistics coordinator not available")

    hass.services.async_register(DOMAIN, "import_statistics", handle_import_statistics)

    return True


async def async_options_updated(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    # Reload the integration to apply new options
    await hass.config_entries.async_reload(entry.entry_id)


async def async_remove_config_entry_device(
        hass: HomeAssistant, config_entry: ConfigEntry, device_entry: device_registry.DeviceEntry
) -> bool:
    return True
