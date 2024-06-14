"""Support for NHC2 Thermostats."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.generic_hvac_climate import Nhc2GenericHvacClimateEntity
from .entities.hvacthermostat_hvac_climate import Nhc2HvacthermostatHvacClimateEntity
from .entities.thermostat_hvac_climate import Nhc2ThermostatHvacClimateEntity
from .entities.thermostat_thermostat_climate import Nhc2ThermostatThermostatClimateEntity
from .entities.virtual_hvac_climate import Nhc2VirtualHvacClimateEntity
from .nhccoco.devices.generic_hvac import CocoGenericHvac
from .nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhccoco.devices.thermostat_hvac import CocoThermostatHvac
from .nhccoco.devices.thermostat_thermostat import CocoThermostatThermostat
from .nhccoco.devices.touchswitch_hvac import CocoTouchswitchHvac
from .nhccoco.devices.virtual_hvac import CocoVirtualHvac
from .nhccoco.devices.virtual_thermostat import CocoVirtualThermostat

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_thermostats'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring climates')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoThermostatHvac)
    device_instances += gateway.get_device_instances(CocoTouchswitchHvac)
    _LOGGER.info('→ Found %s NHC Thermostat (thermostat, touchswitch)', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ThermostatHvacClimateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoHvacthermostatHvac)
    _LOGGER.info('→ Found %s NHC HVAC Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2HvacthermostatHvacClimateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoThermostatThermostat)
    device_instances += gateway.get_device_instances(CocoVirtualThermostat)
    _LOGGER.info('→ Found %s NHC Touch Switch, Virtual Thermostat', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ThermostatThermostatClimateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericHvac)
    _LOGGER.info('→ Found %s Generic Heating/Cooling Implementations', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericHvacClimateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoVirtualHvac)
    _LOGGER.info('→ Found %s NHC Virtual Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2VirtualHvacClimateEntity(device_instance, hub, gateway))

        async_add_entities(entities)
