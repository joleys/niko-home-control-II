import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.audiocontrol_action_speaker import Nhc2AudiocontrolActionSpeakerEntity
from .entities.electricity_clamp_centralmeter_electrical_power import \
    Nhc2ElectricityClampCentralmeterElectricalPowerEntity
from .entities.electricity_clamp_centralmeter_clamp_type import Nhc2ElectricityClampCentralmeterClampTypeEntity
from .entities.electricity_clamp_centralmeter_flow import Nhc2ElectricityClampCentralmeterFlowEntity
from .entities.electricity_clamp_centralmeter_segment import Nhc2ElectricityClampCentralmeterSegmentEntity
from .entities.garagedoor_action_basicstate import Nhc2GaragedoorActionBasicStateEntity
from .entities.generic_domestichotwaterunit_coupling_status import Nhc2GenericDomestichotwaterunitCouplingStatusEntity
from .entities.generic_energyhome_electrical_power_consumption import \
    Nhc2GenericEnergyhomeElectricalPowerConsumptionEntity
from .entities.generic_energyhome_electrical_power_from_grid import Nhc2GenericEnergyhomeElectricalPowerFromGridEntity
from .entities.generic_energyhome_electrical_power_production import \
    Nhc2GenericEnergyhomeElectricalPowerProductionEntity
from .entities.generic_energyhome_electrical_power_self_consumption import \
    Nhc2GenericEnergyhomeElectricalPowerSelfConsumptionEntity
from .entities.generic_energyhome_electrical_power_to_grid import Nhc2GenericEnergyhomeElectricalPowerToGridEntity
from .entities.generic_hvac_coupling_status import Nhc2GenericHvacCouplingStatusEntity
from .entities.generic_smartplug_electrical_power import Nhc2GenericSmartplugElectricalPowerEntity
from .entities.hvacthermostat_hvac_setpoint_temperature import Nhc2HvacthermostatHvacSetpointTemperatureEntity
from .entities.hvacthermostat_hvac_overrule_setpoint import Nhc2HvacthermostatHvacOverruleSetpointEntity
from .entities.hvacthermostat_hvac_overrule_time import Nhc2HvacthermostatHvacOverruleTimeEntity
from .entities.motor_action_last_direction import Nhc2MotorActionLastDirectionEntity
from .entities.naso_smartplug_electrical_power import Nhc2NasoSmartplugElectricalPowerEntity
from .entities.reynaers_action_status import Nhc2ReynaersActionStatusEntity
from .entities.simulation_action_basicstate import Nhc2SimulationActionBasicStateEntity
from .entities.thermostat_hvac_setpoint_temperature import Nhc2ThermostatHvacSetpointTemperatureEntity
from .entities.thermostat_hvac_overrule_time import Nhc2ThermostatHvacOverruleTimeEntity
from .entities.thermostat_hvac_overrule_setpoint import Nhc2ThermostatHvacOverruleSetpointEntity
from .entities.thermostat_thermostat_setpoint_temperature import Nhc2ThermostatThermostatSetpointTemperatureEntity
from .entities.thermostat_thermostat_overrule_time import Nhc2ThermostatThermostatOverruleTimeEntity
from .entities.thermostat_thermostat_overrule_setpoint import Nhc2ThermostatThermostatOverruleSetpointEntity
from .nhccoco.devices.audiocontrol_action import CocoAudiocontrolAction
from .nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .nhccoco.devices.gate_action import CocoGateAction
from .nhccoco.devices.garagedoor_action import CocoGaragedoorAction
from .nhccoco.devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit
from .nhccoco.devices.generic_energyhome import CocoGenericEnergyhome
from .nhccoco.devices.generic_hvac import CocoGenericHvac
from .nhccoco.devices.generic_smartplug import CocoGenericSmartplug
from .nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhccoco.devices.naso_smartplug import CocoNasoSmartplug
from .nhccoco.devices.reynaers_action import CocoReynaersAction
from .nhccoco.devices.rolldownshutter_action import CocoRolldownshutterAction
from .nhccoco.devices.simulation_action import CocoSimulationAction
from .nhccoco.devices.sunblind_action import CocoSunblindAction
from .nhccoco.devices.thermostat_hvac import CocoThermostatHvac
from .nhccoco.devices.thermostat_thermostat import CocoThermostatThermostat
from .nhccoco.devices.touchswitch_hvac import CocoTouchswitchHvac
from .nhccoco.devices.venetianblind_action import CocoVenetianblindAction

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_sensors'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring sensors')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoAudiocontrolAction)
    _LOGGER.info('→ Found %s NHC Audio Control Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AudiocontrolActionSpeakerEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGaragedoorAction)
    _LOGGER.info('→ Found %s NHC Garage Door Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GaragedoorActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoHvacthermostatHvac)
    _LOGGER.info('→ Found %s NHC HVAC Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2HvacthermostatHvacSetpointTemperatureEntity(device_instance, hub, gateway))
            entities.append(Nhc2HvacthermostatHvacOverruleTimeEntity(device_instance, hub, gateway))
            entities.append(Nhc2HvacthermostatHvacOverruleSetpointEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoThermostatHvac)
    device_instances += gateway.get_device_instances(CocoTouchswitchHvac)
    _LOGGER.info('→ Found %s NHC Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ThermostatHvacSetpointTemperatureEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatHvacOverruleTimeEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatHvacOverruleSetpointEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoThermostatThermostat)
    _LOGGER.info('→ Found %s NHC Touch Switch', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ThermostatThermostatSetpointTemperatureEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatThermostatOverruleSetpointEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatThermostatOverruleTimeEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGateAction)
    device_instances += gateway.get_device_instances(CocoRolldownshutterAction)
    device_instances += gateway.get_device_instances(CocoSunblindAction)
    device_instances += gateway.get_device_instances(CocoVenetianblindAction)
    _LOGGER.info('→ Found %s NHC Motor Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            if device_instance.supports_last_direction:
                entities.append(Nhc2MotorActionLastDirectionEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoSimulationAction)
    _LOGGER.info('→ Found %s NHC Presence Simulation Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2SimulationActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoReynaersAction)
    _LOGGER.info('→ Found %s NHC Reynaers Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ReynaersActionStatusEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoNasoSmartplug)
    _LOGGER.info('→ Found %s NHC Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2NasoSmartplugElectricalPowerEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericSmartplug)
    _LOGGER.info('→ Found %s Generic Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericSmartplugElectricalPowerEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoElectricityClampCentralmeter)
    _LOGGER.info('→ Found %s Electricity Metering modules', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ElectricityClampCentralmeterElectricalPowerEntity(device_instance, hub, gateway))
            entities.append(Nhc2ElectricityClampCentralmeterFlowEntity(device_instance, hub, gateway))
            entities.append(Nhc2ElectricityClampCentralmeterSegmentEntity(device_instance, hub, gateway))
            if device_instance.supports_clamp_type:
                entities.append(Nhc2ElectricityClampCentralmeterClampTypeEntity(device_instance, hub, gateway))


        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericEnergyhome)
    _LOGGER.info('→ Found %s Energy Home\'s', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericEnergyhomeElectricalPowerToGridEntity(device_instance, hub, gateway))
            entities.append(Nhc2GenericEnergyhomeElectricalPowerFromGridEntity(device_instance, hub, gateway))
            entities.append(Nhc2GenericEnergyhomeElectricalPowerProductionEntity(device_instance, hub, gateway))
            entities.append(Nhc2GenericEnergyhomeElectricalPowerSelfConsumptionEntity(device_instance, hub, gateway))
            entities.append(Nhc2GenericEnergyhomeElectricalPowerConsumptionEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericHvac)
    _LOGGER.info('→ Found %s Generic Heating/Cooling Implementations', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericHvacCouplingStatusEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericDomestichotwaterunit)
    _LOGGER.info('→ Found %s Generic Warm Water Implementations', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(
                Nhc2GenericDomestichotwaterunitCouplingStatusEntity(device_instance, hub, gateway)
            )

        async_add_entities(entities)
