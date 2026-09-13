"""Support for NHC2 locks."""
import logging

from .nhccoco.coco import CoCo

from .entities.accesscontrol_action_lock import Nhc2AccesscontrolActionLockEntity
from .entities.bellbutton_action_lock import Nhc2BellbuttonActionLockEntity
from .nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction
from .nhccoco.devices.bellbutton_action import CocoBellbuttonAction

from .const import KEY_GATEWAY

from .hub import async_get_hub

KEY_ENTITY = 'nhc2_locks'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring locks')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = async_get_hub(hass, config_entry)

    device_instances = gateway.get_device_instances(CocoAccesscontrolAction)
    _LOGGER.info('→ Found %s NHC Access Control Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            if(device_instance.supports_doorlock):
                entities.append(Nhc2AccesscontrolActionLockEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoBellbuttonAction)
    _LOGGER.info('→ Found %s NHC BellButton Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2BellbuttonActionLockEntity(device_instance, hub, gateway))

        async_add_entities(entities)
