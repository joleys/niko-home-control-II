"""Support for NHC2 lights."""
import logging

import voluptuous as vol

from homeassistant.const import CONF_USERNAME
from homeassistant.helpers import entity_platform

from .nhccoco.coco import CoCo

from .entities.relay_action_light import Nhc2RelayActionLightEntity
from .nhccoco.devices.light_action import CocoLightAction
from .nhccoco.devices.dimmer_action import CocoDimmerAction

from .const import DOMAIN, KEY_GATEWAY, SERVICE_SET_LIGHT_BRIGHTNESS, ATTR_LIGHT_BRIGHTNESS

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_lights'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring lights')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = []
    device_instances += gateway.get_device_instances(CocoLightAction)
    device_instances += gateway.get_device_instances(CocoDimmerAction)

    _LOGGER.info('→ Found %s lights/dimmers', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2RelayActionLightEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SET_LIGHT_BRIGHTNESS,
        {
            vol.Required(ATTR_LIGHT_BRIGHTNESS): vol.Range(0, 100)
        },
        '_service_set_light_brightness',
    )
