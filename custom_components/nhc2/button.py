"""Support for NHC2 buttons."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.alloff_action_button import Nhc2AlloffActionButtonEntity
from .entities.comfort_action_button import Nhc2ComfortActionButtonEntity
from .nhccoco.devices.alloff_action import CocoAlloffAction
from .nhccoco.devices.comfort_action import CocoComfortAction

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_buttons'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring buttons')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoAlloffAction)
    _LOGGER.info('→ Found %s NHC Alloff Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AlloffActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoComfortAction)
    _LOGGER.info('→ Found %s NHC Mood Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ComfortActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)
