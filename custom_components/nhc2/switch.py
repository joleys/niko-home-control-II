"""Support for NHC2 switches."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.alloff_action_basicstate import Nhc2AlloffActionBasicStateEntity
from .entities.comfort_action_basicstate import Nhc2ComfortActionBasicStateEntity
from .entities.flag_action_switch import Nhc2FlagActionSwitchEntity
from .entities.generic_action_basicstate import Nhc2GenericActionBasicStateEntity
from .entities.generic_domestichotwaterunit_boost import Nhc2GenericDomestichotwaterunitBoostEntity
from .entities.generic_hvac_overrule_active import Nhc2GenericHvacOverruleActiveEntity
from .entities.hvacthermostat_hvac_ecosave import Nhc2HvacthermostatHvacEcoSaveEntity
from .entities.hvacthermostat_hvac_thermostat_on import Nhc2HvacthermostatHvacThermostatOnEntity
from .entities.hvacthermostat_hvac_overrule_active import Nhc2HvacthermostatHvacOverruleActiveEntity
from .entities.hvacthermostat_hvac_protect_mode import Nhc2HvacthermostatHvacProtectModeEntity
from .entities.overallcomfort_action_basicstate import Nhc2OverallcomfortActionBasicStateEntity
from .entities.pir_action_basicstate import Nhc2PirActionBasicStateEntity
from .entities.relay_action_switch import Nhc2RelayActionSwitchEntity
from .entities.simulation_action_basicstate_switch import Nhc2SimulationActionBasicStateSwitchEntity
from .entities.thermostat_hvac_ecosave import Nhc2ThermostatHvacEcoSaveEntity
from .entities.thermostat_hvac_overrule_active import Nhc2ThermostatHvacOverruleActiveEntity
from .entities.thermostat_thermostat_ecosave import Nhc2ThermostatThermostatEcoSaveEntity
from .entities.thermostat_thermostat_overrule_active import Nhc2ThermostatThermostatOverruleActiveEntity
from .nhccoco.devices.alloff_action import CocoAlloffAction
from .nhccoco.devices.comfort_action import CocoComfortAction
from .nhccoco.devices.flag_action import CocoFlagAction
from .nhccoco.devices.generic_action import CocoGenericAction
from .nhccoco.devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit
from .nhccoco.devices.generic_hvac import CocoGenericHvac
from .nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhccoco.devices.overallcomfort_action import CocoOverallcomfortAction
from .nhccoco.devices.pir_action import CocoPirAction
from .nhccoco.devices.simulation_action import CocoSimulationAction
from .nhccoco.devices.socket_action import CocoSocketAction
from .nhccoco.devices.switched_fan_action import CocoSwitchedFanAction
from .nhccoco.devices.switched_generic_action import CocoSwitchedGenericAction
from .nhccoco.devices.thermostat_hvac import CocoThermostatHvac
from .nhccoco.devices.thermostat_thermostat import CocoThermostatThermostat
from .nhccoco.devices.touchswitch_hvac import CocoTouchswitchHvac

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_switches'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring switches')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoAlloffAction)
    _LOGGER.info('→ Found %s NHC All Off Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AlloffActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericAction)
    _LOGGER.info('→ Found %s NHC Free Start Stop Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoOverallcomfortAction)
    _LOGGER.info('→ Found %s NHC House Mode Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2OverallcomfortActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoHvacthermostatHvac)
    _LOGGER.info('→ Found %s NHC HVAC Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2HvacthermostatHvacOverruleActiveEntity(device_instance, hub, gateway))
            entities.append(Nhc2HvacthermostatHvacEcoSaveEntity(device_instance, hub, gateway))
            entities.append(Nhc2HvacthermostatHvacThermostatOnEntity(device_instance, hub, gateway))
            entities.append(Nhc2HvacthermostatHvacProtectModeEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoThermostatHvac)
    device_instances += gateway.get_device_instances(CocoTouchswitchHvac)
    _LOGGER.info('→ Found %s NHC Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ThermostatHvacOverruleActiveEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatHvacEcoSaveEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoThermostatThermostat)
    _LOGGER.info('→ Found %s NHC Touch Switch', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ThermostatThermostatEcoSaveEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatThermostatOverruleActiveEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoComfortAction)
    _LOGGER.info('→ Found %s NHC Mood Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ComfortActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoPirAction)
    _LOGGER.info('→ Found %s NHC PIR Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2PirActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoSimulationAction)
    _LOGGER.info('→ Found %s NHC Presence Simulation Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2SimulationActionBasicStateSwitchEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoFlagAction)
    _LOGGER.info('→ Found %s NHC Virtual flags', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2FlagActionSwitchEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoSocketAction)
    device_instances += gateway.get_device_instances(CocoSwitchedFanAction)
    device_instances += gateway.get_device_instances(CocoSwitchedGenericAction)
    _LOGGER.info('→ Found %s NHC Relay Actions (socket, switched-fan, switched-generic)', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2RelayActionSwitchEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericHvac)
    _LOGGER.info('→ Found %s Generic Heating/Cooling Implementations', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericHvacOverruleActiveEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericDomestichotwaterunit)
    _LOGGER.info('→ Found %s Generic Warm Water Implementation', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(
                Nhc2GenericDomestichotwaterunitBoostEntity(device_instance, hub, gateway)
            )

        async_add_entities(entities)
