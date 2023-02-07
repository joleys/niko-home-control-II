"""Support for NHC2 Covers."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.garagedoor_action_cover import Nhc2GaragedoorActionCoverEntity
from .entities.motor_action_cover import Nhc2MotorActionCoverEntity
from .entities.reynaers_action_cover import Nhc2ReynaersActionCoverEntity
from .entities.velux_action_cover import Nhc2VeluxActionCoverEntity
from .nhccoco.devices.garagedoor_action import CocoGaragedoorAction
from .nhccoco.devices.gate_action import CocoGateAction
from .nhccoco.devices.reynaers_action import CocoReynaersAction
from .nhccoco.devices.rolldownshutter_action import CocoRolldownshutterAction
from .nhccoco.devices.sunblind_action import CocoSunblindAction
from .nhccoco.devices.velux_action import CocoVeluxAction
from .nhccoco.devices.venetianblind_action import CocoVenetianblindAction

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_covers'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring covers')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoGaragedoorAction)
    _LOGGER.info('→ Found %s NHC Garage Door Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GaragedoorActionCoverEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGateAction)
    device_instances += gateway.get_device_instances(CocoRolldownshutterAction)
    device_instances += gateway.get_device_instances(CocoSunblindAction)
    device_instances += gateway.get_device_instances(CocoVenetianblindAction)
    _LOGGER.info('→ Found %s NHC Motor Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2MotorActionCoverEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoReynaersAction)
    _LOGGER.info('→ Found %s NHC Reynaers Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ReynaersActionCoverEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoVeluxAction)
    _LOGGER.info('→ Found %s NHC Velux Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2VeluxActionCoverEntity(device_instance, hub, gateway))

        async_add_entities(entities)
