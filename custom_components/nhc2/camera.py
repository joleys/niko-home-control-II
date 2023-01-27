"""Support for NHC2 Camera's."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.accesscontrol_action_camera import Nhc2AccesscontrolActionCameraEntity
from .nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_cameras'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring cameras')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoAccesscontrolAction)
    _LOGGER.info('→ Found %s Access Control Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AccesscontrolActionCameraEntity(device_instance, hub, gateway))

        async_add_entities(entities)
