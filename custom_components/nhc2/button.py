"""Support for NHC2 Buttons."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.accesscontrol_action_button import Nhc2AccesscontrolActionButtonEntity
from .entities.alloff_action_button import Nhc2AlloffActionButtonEntity
from .entities.bellbutton_action_button import Nhc2BellbuttonActionButtonEntity
from .entities.comfort_action_button import Nhc2ComfortActionButtonEntity
from .entities.generic_action_button import Nhc2GenericActionButtonEntity
from .entities.overallcomfort_action_button import Nhc2OverallcomfortActionButtonEntity
from .nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction
from .nhccoco.devices.alloff_action import CocoAlloffAction
from .nhccoco.devices.bellbutton_action import CocoBellbuttonAction
from .nhccoco.devices.comfort_action import CocoComfortAction
from .nhccoco.devices.generic_action import CocoGenericAction
from .nhccoco.devices.overallcomfort_action import CocoOverallcomfortAction

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_buttons'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring buttons')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoAccesscontrolAction)
    _LOGGER.info('→ Found %s NHC Access Control Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AccesscontrolActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoAlloffAction)
    _LOGGER.info('→ Found %s NHC All Off Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AlloffActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoBellbuttonAction)
    _LOGGER.info('→ Found %s NHC BellButton Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2BellbuttonActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericAction)
    _LOGGER.info('→ Found %s NHC Free Start Stop Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoOverallcomfortAction)
    _LOGGER.info('→ Found %s NHC House Mode Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2OverallcomfortActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoComfortAction)
    _LOGGER.info('→ Found %s NHC Mood Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ComfortActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)
