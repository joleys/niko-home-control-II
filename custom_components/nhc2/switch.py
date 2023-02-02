"""Support for NHC2 switches."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.flag_action_switch import Nhc2FlagActionSwitchEntity
from .entities.hvacthermostat_hvac_ecosave import Nhc2HvacthermostatHvacEcoSaveEntity
from .entities.hvacthermostat_hvac_thermostat_on import Nhc2HvacthermostatHvacThermostatOnEntity
from .entities.hvacthermostat_hvac_overrule_active import Nhc2HvacthermostatHvacOverruleActiveEntity
from .entities.hvacthermostat_hvac_protect_mode import Nhc2HvacthermostatHvacProtectModeEntity
from .entities.relay_action_switch import Nhc2RelayActionSwitchEntity
from .entities.thermostat_hvac_ecosave import Nhc2ThermostatHvacEcoSaveEntity
from .entities.thermostat_hvac_overrule_active import Nhc2ThermostatHvacOverruleActiveEntity
from .nhccoco.devices.flag_action import CocoFlagAction
from .nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhccoco.devices.socket_action import CocoSocketAction
from .nhccoco.devices.switched_fan_action import CocoSwitchedFanAction
from .nhccoco.devices.switched_generic_action import CocoSwitchedGenericAction
from .nhccoco.devices.thermostat_hvac import CocoThermostatHvac
from .nhccoco.devices.touchswitch_hvac import CocoTouchswitchHvac

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_switches'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring switches')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

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
