"""Support for NHC2 Camera's."""
import logging

from .nhccoco.coco import CoCo

from .entities.robinsip_videodoorstation_camera import Nhc2RobinsipVideodoorstationCameraEntity
from .nhccoco.devices.robinsip_videodoorstation import CocoRobinsipVideodoorstation

from .const import KEY_GATEWAY

from .hub import async_get_hub

KEY_ENTITY = 'nhc2_cameras'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring cameras')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = async_get_hub(hass, config_entry)

    device_instances = gateway.get_device_instances(CocoRobinsipVideodoorstation)
    _LOGGER.info('→ Found %s Robinsip Videodoorstations (undocumented)', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2RobinsipVideodoorstationCameraEntity(device_instance, hub, gateway))

        async_add_entities(entities)
