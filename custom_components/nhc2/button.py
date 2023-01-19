"""Support for NHC2 Buttons."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.alloff_action_button import Nhc2AlloffActionButtonEntity
from .nhccoco.devices.alloff_action import CocoAlloffAction

from .const import DOMAIN, KEY_GATEWAY

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_switches'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = []
    device_instances += gateway.get_device_instances(CocoAlloffAction)

    _LOGGER.info('Found %s buttons', len(device_instances))
    if len(device_instances) > 0:
        async_add_entities([
            Nhc2AlloffActionButtonEntity(device_instance, hub, gateway) for device_instance in device_instances
        ])
