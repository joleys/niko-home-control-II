"""Support for NHC2 switches."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.relay_action_switch import Nhc2RelayActionSwitchEntity
from .nhccoco.devices.socket_action import CocoSocketAction
from .nhccoco.devices.switched_fan_action import CocoSwitchedFanAction
from .nhccoco.devices.switched_generic_action import CocoSwitchedGenericAction

from .const import DOMAIN, KEY_GATEWAY

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_switches'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring switches')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = []
    device_instances += gateway.get_device_instances(CocoSocketAction)
    device_instances += gateway.get_device_instances(CocoSwitchedFanAction)
    device_instances += gateway.get_device_instances(CocoSwitchedGenericAction)
    device_instances += gateway.get_device_instances(CocoSwitchedGenericAction)

    _LOGGER.info('→ Found %s switches', len(device_instances))
    if len(device_instances) > 0:
        async_add_entities([
            Nhc2RelayActionSwitchEntity(device_instance, hub, gateway) for device_instance in device_instances
        ])
