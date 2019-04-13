"""Support for NHC2."""
import asyncio
import logging
import os

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.util.json import load_json

from .config_flow import Nhc2FlowHandler
from .const import DOMAIN

REQUIREMENTS = ['paho-mqtt==1.4.0']

_LOGGER = logging.getLogger(__name__)

DOMAIN = DOMAIN
CONFIG_FILE = '.nhc2_psk.conf'
KEY_GATEWAY = 'nhc2_gateway'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.port,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up the NHC2 component."""
    conf = config.get(DOMAIN)

    if conf is None:
        return True

    configured_hosts = [entry.data['host'] for entry in
                        hass.config_entries.async_entries(DOMAIN)]

    legacy_hosts = await hass.async_add_executor_job(
        load_json, hass.config.path(CONFIG_FILE))

    for host, info in legacy_hosts.items():
        if host in configured_hosts:
            continue

        info[CONF_HOST] = host

        hass.async_create_task(hass.config_entries.flow.async_init(
            DOMAIN, context={'source': config_entries.SOURCE_IMPORT},
            data=info
        ))

    host = conf.get(CONF_HOST)
    port = conf.get(CONF_PORT)
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)

    if host is None or host in configured_hosts or host in legacy_hosts:
        return True

    hass.async_create_task(hass.config_entries.flow.async_init(
        DOMAIN, context={'source': config_entries.SOURCE_IMPORT},
        data={CONF_HOST: host, CONF_PORT: port,
              CONF_USERNAME: username,
              CONF_PASSWORD: password}
    ))

    return True

def nhc2_get_sysinfo(loop, _nhc2):
    fut = loop.create_future()
    _nhc2.get_systeminfo(
        lambda sys_info: fut.set_result(sys_info)
    )
    return fut

async def _get_systinfo(hass, gateway):
    return await nhc2_get_sysinfo(hass.loop, gateway)


async def async_setup_entry(hass, entry):
    """Create a NHC2 gateway."""
    # host, identity, key, allow_tradfri_groups
    from .nhc2 import NHC2

    gateway = NHC2(
        entry.data[CONF_HOST],
        entry.data[CONF_PORT],
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        os.path.dirname(os.path.realpath(__file__)) + '/niko_ca.pem'
    )

    async def on_hass_stop(event):
        """Close connection when hass stops."""
        gateway.disconnect()

    hass.data.setdefault(KEY_GATEWAY, {})[entry.entry_id] = gateway

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)

    _LOGGER.debug('Connecting to %s:%s', entry.data[CONF_HOST], str(entry.data[CONF_PORT]))
    gateway.connect()
    try:
        # NHC2 should respond fast, so there should be no need to wait...
        nhc2_sysinfo = await asyncio.wait_for(_get_systinfo(hass, gateway), timeout=20.0)
        _LOGGER.debug('Retrieved sysinfo')
        params = nhc2_sysinfo['Params']
        system_info = next(filter((lambda x: x and 'SystemInfo' in x), params), None)['SystemInfo']
        s_w_versions = next(filter((lambda x: x and 'SWversions' in x), system_info), None)['SWversions']
        coco_image = next(filter((lambda x: x and 'CocoImage' in x), s_w_versions), None)['CocoImage']
        nhc_version = next(filter((lambda x: x and 'NhcVersion' in x), s_w_versions), None)['NhcVersion']

        _LOGGER.debug('Sysinfo: NhcVersion %s - CocoImage %s', nhc_version, coco_image)

        dev_reg = await hass.helpers.device_registry.async_get_registry()
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

        hass.async_create_task(hass.config_entries.async_forward_entry_setup(
            entry, 'light'
        ))

        hass.async_create_task(hass.config_entries.async_forward_entry_setup(
            entry, 'switch'
        ))
        return True
    except asyncio.TimeoutError:

        _LOGGER.debug('Connection to %s:%s FAILED :(', entry.data[CONF_HOST], str(entry.data[CONF_PORT]))
        return False

