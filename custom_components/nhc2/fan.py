"""Support for NHC2 Fans."""
import logging

from .nhccoco.coco import CoCo

from .entities.fan_action_fan import Nhc2FanActionFanEntity
from .entities.generic_fan_fan import Nhc2GenericFanFanEntity
from .nhccoco.devices.fan_action import CocoFanAction
from .nhccoco.devices.generic_fan import CocoGenericFan

from .const import KEY_GATEWAY

from .hub import async_get_hub

KEY_ENTITY = 'nhc2_fans'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring fans')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = async_get_hub(hass, config_entry)

    device_instances = gateway.get_device_instances(CocoFanAction)
    _LOGGER.info('→ Found %s NHC Fan Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2FanActionFanEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericFan)
    _LOGGER.info('→ Found %s Generic Ventilation Implementation', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericFanFanEntity(device_instance, hub, gateway))

        async_add_entities(entities)
