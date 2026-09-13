"""Support for NHC2 update sensors."""
import logging

from .nhccoco.coco import CoCo

from .nhccoco.devices.controller import CocoController
from .entities.controller_latest_config_loaded_updated import Nhc2ControllerLatestConfigLoadedUpdateEntity

from .const import KEY_GATEWAY

from .hub import async_get_hub

KEY_ENTITY = 'nhc2_update_sensors'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring update sensors')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = async_get_hub(hass, config_entry)

    device_instances = gateway.get_device_instances(CocoController)
    _LOGGER.info('→ Found %s Controllers', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ControllerLatestConfigLoadedUpdateEntity(device_instance, hub, gateway))

        async_add_entities(entities)
