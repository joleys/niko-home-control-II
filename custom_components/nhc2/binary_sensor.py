import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.alloff_action_active import Nhc2AlloffActionActiveEntity
from .entities.alloff_action_basicstate import Nhc2AlloffActionBasicStateEntity
from .entities.dimmer_action_alligned import Nhc2DimmerActionAlignedEntity
from .nhccoco.devices.alloff_action import CocoAlloffAction
from .nhccoco.devices.dimmer_action import CocoDimmerAction

from .const import DOMAIN, KEY_GATEWAY

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_binary_sensors'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoDimmerAction)
    _LOGGER.info('Found %s dimmers', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2DimmerActionAlignedEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoAlloffAction)
    _LOGGER.info('Found %s alloffs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AlloffActionActiveEntity(device_instance, hub, gateway))
            entities.append(Nhc2AlloffActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)
