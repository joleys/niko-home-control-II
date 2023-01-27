import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.electricity_clamp_centralmeter_electrical_power import \
    Nhc2ElectricityClampCentralmeterElectricalPowerEntity
from .entities.electricity_clamp_centralmeter_clamp_type import Nhc2ElectricityClampCentralmeterClampTypeEntity
from .entities.electricity_clamp_centralmeter_flow import Nhc2ElectricityClampCentralmeterFlowEntity
from .entities.electricity_clamp_centralmeter_segment import Nhc2ElectricityClampCentralmeterSegmentEntity
from .entities.garagedoor_action_basicstate import Nhc2GaragedoorActionBasicStateEntity
from .entities.generic_energyhome_electrical_power_consumption import \
    Nhc2GenericEnergyhomeElectricalPowerConsumptionEntity
from .entities.generic_energyhome_electrical_power_from_grid import Nhc2GenericEnergyhomeElectricalPowerFromGridEntity
from .entities.generic_energyhome_electrical_power_production import \
    Nhc2GenericEnergyhomeElectricalPowerProductionEntity
from .entities.generic_energyhome_electrical_power_self_consumption import \
    Nhc2GenericEnergyhomeElectricalPowerSelfConsumptionEntity
from .entities.generic_energyhome_electrical_power_to_grid import Nhc2GenericEnergyhomeElectricalPowerToGridEntity
from .entities.hvacthermostat_hvac_setpoint_temperature import Nhc2HvacthermostatHvacSetpointTemperatureEntity
from .entities.hvacthermostat_hvac_overrule_setpoint import Nhc2HvacthermostatHvacOverruleSetpointEntity
from .entities.hvacthermostat_hvac_overrule_time import Nhc2HvacthermostatHvacOverruleTimeEntity
from .entities.naso_smartplug_electrical_power import Nhc2NasoSmartPlugElectricalPowerEntity
from .entities.thermostat_hvac_setpoint_temperature import Nhc2ThermostatHvacSetpointTemperatureEntity
from .entities.thermostat_hvac_overrule_time import Nhc2ThermostatHvacOverruleTimeEntity
from .entities.thermostat_hvac_overrule_setpoint import Nhc2ThermostatHvacOverruleSetpointEntity
from .nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .nhccoco.devices.garagedoor_action import CocoGaragedoorAction
from .nhccoco.devices.generic_energyhome import CocoGenericEnergyhome
from .nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhccoco.devices.naso_smartplug import CocoNasoSmartplug
from .nhccoco.devices.thermostat_hvac import CocoThermostatHvac
from .nhccoco.devices.touchswitch_hvac import CocoTouchswitchHvac

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_sensors'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring sensors')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoGaragedoorAction)
    _LOGGER.info('→ Found %s Garagedoor Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GaragedoorActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoHvacthermostatHvac)
    _LOGGER.info('→ Found %s HVAC Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2HvacthermostatHvacSetpointTemperatureEntity(device_instance, hub, gateway))
            entities.append(Nhc2HvacthermostatHvacOverruleTimeEntity(device_instance, hub, gateway))
            entities.append(Nhc2HvacthermostatHvacOverruleSetpointEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoThermostatHvac)
    device_instances += gateway.get_device_instances(CocoTouchswitchHvac)
    _LOGGER.info('→ Found %s Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ThermostatHvacSetpointTemperatureEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatHvacOverruleTimeEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatHvacOverruleSetpointEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoNasoSmartplug)
    _LOGGER.info('→ Found %s Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2NasoSmartPlugElectricalPowerEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoElectricityClampCentralmeter)
    _LOGGER.info('→ Found %s Electricity Metering modules', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ElectricityClampCentralmeterElectricalPowerEntity(device_instance, hub, gateway))
            entities.append(Nhc2ElectricityClampCentralmeterClampTypeEntity(device_instance, hub, gateway))
            entities.append(Nhc2ElectricityClampCentralmeterFlowEntity(device_instance, hub, gateway))
            entities.append(Nhc2ElectricityClampCentralmeterSegmentEntity(device_instance, hub, gateway))

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
