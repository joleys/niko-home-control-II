"""Support for NHC2 Buttons."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.accesscontrol_action_button import Nhc2AccesscontrolActionButtonEntity
from .entities.bellbutton_action_button import Nhc2BellbuttonActionButtonEntity
from .entities.pir_action_button import Nhc2PirActionButtonEntity
from .entities.simulation_action_button import Nhc2SimulationActionButtonEntity
from .nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction
from .nhccoco.devices.bellbutton_action import CocoBellbuttonAction
from .nhccoco.devices.pir_action import CocoPirAction
from .nhccoco.devices.simulation_action import CocoSimulationAction

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

    device_instances = gateway.get_device_instances(CocoBellbuttonAction)
    _LOGGER.info('→ Found %s NHC BellButton Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2BellbuttonActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoPirAction)
    _LOGGER.info('→ Found %s NHC PIR Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2PirActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoSimulationAction)
    _LOGGER.info('→ Found %s NHC Presence Simulation Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2SimulationActionButtonEntity(device_instance, hub, gateway))

        async_add_entities(entities)
