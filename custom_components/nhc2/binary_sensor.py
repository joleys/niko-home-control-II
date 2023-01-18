import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.dimmers_are_alligned import Nhc2DimmersAreAlignedEntity
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
    _LOGGER.info('Found %s devices', len(device_instances))

    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            if isinstance(device_instance, CocoDimmerAction):
                entities.append(Nhc2DimmersAreAlignedEntity(device_instance, hub, gateway))

        async_add_entities(entities)
