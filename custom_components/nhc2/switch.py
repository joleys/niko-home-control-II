"""Support for NHC2 switches."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.accesscontrol_action_basicstate_switch import Nhc2AccesscontrolActionBasicStateSwitchEntity
from .entities.bellbutton_action_basicstate_switch import Nhc2BellbuttonActionBasicStateSwitchEntity
from .entities.condition_action_switch import Nhc2ConditionActionSwitchEntity
from .entities.flag_action_switch import Nhc2FlagActionSwitchEntity
from .entities.electricity_clamp_centralmeter_disable_report_instant_usage_re_enabling import \
    Nhc2ElectricityClampCentralmeterDisableReportInstantUsageReEnablingEntity
from .entities.generic_action_basicstate import Nhc2GenericActionBasicStateEntity
from .entities.generic_domestichotwaterunit_boost import Nhc2GenericDomestichotwaterunitBoostEntity
from .entities.generic_energyhome_disable_report_instant_usage_re_enabling import \
    Nhc2GenericEnergyhomeDisableReportInstantUsageReEnablingEntity
from .entities.generic_fan_boost import Nhc2GenericFanBoostEntity
from .entities.generic_hvac_overrule_active import Nhc2GenericHvacOverruleActiveEntity
from .entities.generic_smartplug_disable_report_instant_usage_re_enabling import \
    Nhc2GenericSmartplugDisableReportInstantUsageReEnablingEntity
from .entities.generic_smartplug_status import Nhc2GenericSmartplugStatusEntity
from .entities.hvacthermostat_hvac_ecosave import Nhc2HvacthermostatHvacEcoSaveEntity
from .entities.hvacthermostat_hvac_thermostat_on import Nhc2HvacthermostatHvacThermostatOnEntity
from .entities.hvacthermostat_hvac_overrule_active import Nhc2HvacthermostatHvacOverruleActiveEntity
from .entities.hvacthermostat_hvac_protect_mode import Nhc2HvacthermostatHvacProtectModeEntity
from .entities.naso_smartplug_disable_report_instant_usage_re_enabling import \
    Nhc2NasoSmartplugDisableReportInstantUsageReEnablingEntity
from .entities.naso_smartplug_status import Nhc2NasoSmartplugStatusEntity
from .entities.overallcomfort_action_basicstate import Nhc2OverallcomfortActionBasicStateEntity
from .entities.pir_action_basicstate import Nhc2PirActionBasicStateEntity
from .entities.relay_action_switch import Nhc2RelayActionSwitchEntity
from .entities.simulation_action_basicstate_switch import Nhc2SimulationActionBasicStateSwitchEntity
from .entities.thermostat_hvac_ecosave import Nhc2ThermostatHvacEcoSaveEntity
from .entities.thermostat_hvac_overrule_active import Nhc2ThermostatHvacOverruleActiveEntity
from .entities.thermostat_thermostat_ecosave import Nhc2ThermostatThermostatEcoSaveEntity
from .entities.thermostat_thermostat_overrule_active import Nhc2ThermostatThermostatOverruleActiveEntity
from .nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction
from .nhccoco.devices.bellbutton_action import CocoBellbuttonAction
from .nhccoco.devices.condition_action import CocoConditionAction
from .nhccoco.devices.flag_action import CocoFlagAction
from .nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .nhccoco.devices.generic_action import CocoGenericAction
from .nhccoco.devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit
from .nhccoco.devices.generic_energyhome import CocoGenericEnergyhome
from .nhccoco.devices.generic_fan import CocoGenericFan
from .nhccoco.devices.generic_hvac import CocoGenericHvac
from .nhccoco.devices.generic_smartplug import CocoGenericSmartplug
from .nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhccoco.devices.naso_smartplug import CocoNasoSmartplug
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

    device_instances = gateway.get_device_instances(CocoAccesscontrolAction)
    _LOGGER.info('→ Found %s NHC Access Control Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            if device_instance.supports_basicstate:
                entities.append(Nhc2AccesscontrolActionBasicStateSwitchEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoBellbuttonAction)
    _LOGGER.info('→ Found %s NHC BellButton Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2BellbuttonActionBasicStateSwitchEntity(device_instance, hub, gateway))

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
    _LOGGER.info('→ Found %s NHC Thermostat (thermostat, touchswitch)', len(device_instances))
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

    device_instances = gateway.get_device_instances(CocoNasoSmartplug)
    _LOGGER.info('→ Found %s NHC Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2NasoSmartplugDisableReportInstantUsageReEnablingEntity(device_instance, hub, gateway))
            if device_instance.supports_status:
                entities.append(Nhc2NasoSmartplugStatusEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericSmartplug)
    _LOGGER.info('→ Found %s Generic Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(
                Nhc2GenericSmartplugDisableReportInstantUsageReEnablingEntity(device_instance, hub, gateway)
            )

            if device_instance.supports_status:
                entities.append(Nhc2GenericSmartplugStatusEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoElectricityClampCentralmeter)
    _LOGGER.info('→ Found %s Electricity Metering modules', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(
                Nhc2ElectricityClampCentralmeterDisableReportInstantUsageReEnablingEntity(
                    device_instance, hub, gateway
                )
            )

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericEnergyhome)
    _LOGGER.info('→ Found %s Energy Home\'s', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(
                Nhc2GenericEnergyhomeDisableReportInstantUsageReEnablingEntity(device_instance, hub, gateway)
            )

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericFan)
    _LOGGER.info('→ Found %s Generic Ventilation Implementation', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            if device_instance.supports_boost:
                entities.append(Nhc2GenericFanBoostEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericHvac)
    _LOGGER.info('→ Found %s Generic Heating/Cooling Implementations', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            if device_instance.supports_overrule_active:
                entities.append(Nhc2GenericHvacOverruleActiveEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericDomestichotwaterunit)
    _LOGGER.info('→ Found %s Generic Warm Water Implementation', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericDomestichotwaterunitBoostEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoConditionAction)
    _LOGGER.info('→ Found %s Condition actions (undocumented)', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ConditionActionSwitchEntity(device_instance, hub, gateway))

        async_add_entities(entities)
