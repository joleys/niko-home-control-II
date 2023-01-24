import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.naso_smartplug_electrical_power import Nhc2NasoSmartPlugElectricalPowerEntity
from .entities.thermostat_hvac_setpoint_temperature import Nhc2ThermostatHvacSetpointTemperatureEntity
from .entities.thermostat_hvac_overrule_time import Nhc2ThermostatHvacOverruleTimeEntity
from .entities.thermostat_hvac_overrule_setpoint import Nhc2ThermostatHvacOverruleSetpointEntity
from .nhccoco.devices.naso_smartplug import CocoNasoSmartplug
from .nhccoco.devices.thermostat_hvac import CocoThermostatHvac
from .nhccoco.devices.touchswitch_hvac import CocoTouchswitchHvac

from .const import DOMAIN, KEY_GATEWAY

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_sensors'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring sensors')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoNasoSmartplug)
    _LOGGER.info('→ Found %s smartplugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2NasoSmartPlugElectricalPowerEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoThermostatHvac)
    device_instances += gateway.get_device_instances(CocoTouchswitchHvac)
    _LOGGER.info('→ Found %s thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ThermostatHvacSetpointTemperatureEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatHvacOverruleTimeEntity(device_instance, hub, gateway))
            entities.append(Nhc2ThermostatHvacOverruleSetpointEntity(device_instance, hub, gateway))

        async_add_entities(entities)
