"""Support for Niko Home Control II - CoCo."""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, \
    CONF_PASSWORD, CONF_ADDRESS, CONF_PORT
from homeassistant.const import EVENT_HOMEASSISTANT_STOP

from .config_flow import Nhc2FlowHandler  # noqa  pylint_disable=unused-import
from .const import DOMAIN, KEY_GATEWAY, CONF_SWITCHES_AS_LIGHTS
from .helpers import extract_versions

_LOGGER = logging.getLogger(__name__)

DOMAIN = DOMAIN
KEY_GATEWAY = KEY_GATEWAY

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_ADDRESS): cv.string,
        vol.Optional(CONF_PORT): vol.All(vol.Coerce(int), vol.Range(min=0, max=65535)),
        vol.Optional(CONF_SWITCHES_AS_LIGHTS, default=False): bool
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
    switches_as_lights = conf.get(CONF_SWITCHES_AS_LIGHTS)

    hass.async_create_task(hass.config_entries.flow.async_init(
        DOMAIN, context={'source': config_entries.SOURCE_IMPORT},
        data={
            CONF_HOST: host,
            CONF_USERNAME: username,
            CONF_PASSWORD: password,
            CONF_ADDRESS: address,
            CONF_PORT: port,
            CONF_SWITCHES_AS_LIGHTS: switches_as_lights
        }
    ))

    return True

FORWARD_PLATFORMS = (
    "climate",
    "switch",
    "light",
    "fan",
    "cover"
)

async def async_setup_entry(hass, entry):
    """Create a NHC2 gateway."""
    from .coco import CoCo
    coco = CoCo(
        address=entry.data[CONF_HOST],
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        port=entry.data[CONF_PORT] if CONF_PORT in entry.data else 8883,
        switches_as_lights=entry.data[CONF_SWITCHES_AS_LIGHTS]
    )



    async def on_hass_stop(event):
        """Close connection when hass stops."""
        coco.disconnect()

    def get_process_sysinfo(dev_reg):
        def process_sysinfo(nhc2_sysinfo):
            coco_image, nhc_version = extract_versions(nhc2_sysinfo)
            _LOGGER.debug('Sysinfo: NhcVersion %s - CocoImage %s',
                          nhc_version,
                          coco_image)
            dev_reg.async_get_or_create(
                config_entry_id=entry.entry_id,
                connections=set(),
                identifiers={
                    (DOMAIN, entry.data[CONF_USERNAME])
                },
                manufacturer='Niko',
                name='Home Control II',
                model='Connected controller',
                sw_version=nhc_version + ' - CoCo Image: ' + coco_image,
            )

            for platform in FORWARD_PLATFORMS:
                _LOGGER.info("Forwarding platform: %s", platform)
                hass.async_create_task(
                    hass.config_entries.async_forward_entry_setup(entry, platform)
                )

        return process_sysinfo

    hass.data.setdefault(KEY_GATEWAY, {})[entry.entry_id] = coco
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)

    _LOGGER.debug('Connecting to %s with %s',
                  entry.data[CONF_HOST], entry.data[CONF_USERNAME]
                  )
    coco.connect()
    dev_reg = await hass.helpers.device_registry.async_get_registry()
    coco.get_systeminfo(get_process_sysinfo(dev_reg))

    return True
