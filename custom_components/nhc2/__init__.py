"""Support for Niko Home Control II - CoCo."""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_ADDRESS, CONF_PORT, \
    EVENT_HOMEASSISTANT_STOP
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry
from homeassistant.core import HomeAssistant

from .config_flow import Nhc2FlowHandler  # noqa  pylint_disable=unused-import
from .const import DOMAIN, KEY_GATEWAY, BRAND
from .nhccoco.helpers import extract_versions
from .nhccoco.const import MQTT_RC_CODES
from .nhccoco.coco import CoCo

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_ADDRESS): cv.string,
        vol.Optional(CONF_PORT): vol.All(vol.Coerce(int), vol.Range(min=0, max=65535))
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up the NHC2 CoCo component."""
    conf = config.get(DOMAIN)

    if conf is None:
        return True

    host = conf.get(CONF_HOST)
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)
    address = conf.get(CONF_ADDRESS)
    port = conf.get(CONF_PORT)

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={'source': config_entries.SOURCE_IMPORT},
            data={
                CONF_HOST: host,
                CONF_USERNAME: username,
                CONF_PASSWORD: password,
                CONF_ADDRESS: address,
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
    "update",
)


async def async_setup_entry(hass, entry):
    """Create a NHC2 gateway."""

    coco = CoCo(
        address=entry.data[CONF_HOST],
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        port=entry.data[CONF_PORT] if CONF_PORT in entry.data else 8883
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

            for platform in FORWARD_PLATFORMS:
                hass.add_job(
                    hass.config_entries.async_forward_entry_setup(entry, platform)
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
            entry.async_start_reauth(hass)

    hass.data.setdefault(KEY_GATEWAY, {})[entry.entry_id] = coco
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)

    dev_reg = device_registry.async_get(hass)
    coco.set_systeminfo_callback(process_sysinfo(dev_reg))
    coco.set_devices_list_callback(reload_entities())

    _LOGGER.debug('Connecting to %s with %s', entry.data[CONF_HOST], entry.data[CONF_USERNAME])
    coco.connect(on_connection_refused)

    return True


async def async_remove_config_entry_device(
        hass: HomeAssistant, config_entry: ConfigEntry, device_entry: device_registry.DeviceEntry
) -> bool:
    return True
