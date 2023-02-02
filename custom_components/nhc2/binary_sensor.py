import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.accesscontrol_action_basicstate import Nhc2AccesscontrolActionBasicStateEntity
from .entities.accesscontrol_action_decline_call_applied_on_all_devices import \
    Nhc2AccesscontrolActionDeclineCallAppliedOnAllDevicesEntity
from .entities.alloff_action_active import Nhc2AlloffActionActiveEntity
from .entities.alloff_action_basicstate import Nhc2AlloffActionBasicStateEntity
from .entities.comfort_action_basicstate import Nhc2ComfortActionBasicStateEntity
from .entities.comfort_action_mood_active import Nhc2ComfortActionMoodActiveEntity
from .entities.dimmer_action_alligned import Nhc2DimmerActionAlignedEntity
from .entities.electricity_clamp_centralmeter_report_instant_usage import \
    Nhc2ElectricityClampCentralmeterReportInstantUsageEntity
from .entities.generic_action_basicstate import Nhc2GenericActionBasicStateEntity
from .entities.generic_action_start_active import Nhc2GenericActionStartActiveEntity
from .entities.generic_energyhome_electrical_power_production_threshold_exceeded import \
    Nhc2GenericEnergyhomeElectricalPowerProductionThresholdExceededEntity
from .entities.generic_energyhome_report_instant_usage import Nhc2GenericEnergyhomeReportInstantUsageEntity
from .entities.generic_smartplug_report_instant_usage import Nhc2GenericSmartPlugReportInstantUsageEntity
from .entities.hvacthermostat_hvac_hvac_on import Nhc2HvacthermostatHvacHvacOnEntity
from .entities.motor_action_cover import Nhc2MotorActionCoverEntity
from .entities.motor_action_moving import Nhc2MotorActionMovingEntity
from .entities.naso_smartplug_feedback_enabled import Nhc2NasoSmartPlugFeedbackEnabledEntity
from .entities.naso_smartplug_measuring_only import Nhc2NasoSmartPlugMeasuringOnlyEntity
from .entities.naso_smartplug_report_instant_usage import Nhc2NasoSmartPlugReportInstantUsageEntity
from .nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction
from .nhccoco.devices.alloff_action import CocoAlloffAction
from .nhccoco.devices.comfort_action import CocoComfortAction
from .nhccoco.devices.dimmer_action import CocoDimmerAction
from .nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .nhccoco.devices.gate_action import CocoGateAction
from .nhccoco.devices.generic_action import CocoGenericAction
from .nhccoco.devices.generic_energyhome import CocoGenericEnergyhome
from .nhccoco.devices.generic_smartplug import CocoGenericSmartplug
from .nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhccoco.devices.naso_smartplug import CocoNasoSmartplug
from .nhccoco.devices.rolldownshutter_action import CocoRolldownshutterAction
from .nhccoco.devices.sunblind_action import CocoSunblindAction
from .nhccoco.devices.venetianblind_action import CocoVenetianblindAction

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_binary_sensors'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring binary sensors')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoAccesscontrolAction)
    _LOGGER.info('→ Found %s Access Control Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AccesscontrolActionBasicStateEntity(device_instance, hub, gateway))
            entities.append(Nhc2AccesscontrolActionDeclineCallAppliedOnAllDevicesEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoAlloffAction)
    _LOGGER.info('→ Found %s All Off Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AlloffActionActiveEntity(device_instance, hub, gateway))
            entities.append(Nhc2AlloffActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoDimmerAction)
    _LOGGER.info('→ Found %s Dimmer Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2DimmerActionAlignedEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericAction)
    _LOGGER.info('→ Found %s NHC Free Start Stop Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericActionBasicStateEntity(device_instance, hub, gateway))
            entities.append(Nhc2GenericActionStartActiveEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoHvacthermostatHvac)
    _LOGGER.info('→ Found %s HVAC Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2HvacthermostatHvacHvacOnEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoComfortAction)
    _LOGGER.info('→ Found %s Mood Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ComfortActionBasicStateEntity(device_instance, hub, gateway))
            entities.append(Nhc2ComfortActionMoodActiveEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGateAction)
    device_instances += gateway.get_device_instances(CocoRolldownshutterAction)
    device_instances += gateway.get_device_instances(CocoSunblindAction)
    device_instances += gateway.get_device_instances(CocoVenetianblindAction)
    _LOGGER.info('→ Found %s Motor Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2MotorActionCoverEntity(device_instance, hub, gateway))
            entities.append(Nhc2MotorActionMovingEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoNasoSmartplug)
    _LOGGER.info('→ Found %s Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2NasoSmartPlugReportInstantUsageEntity(device_instance, hub, gateway))
            entities.append(Nhc2NasoSmartPlugFeedbackEnabledEntity(device_instance, hub, gateway))
            entities.append(Nhc2NasoSmartPlugMeasuringOnlyEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericSmartplug)
    _LOGGER.info('→ Found %s Generic Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericSmartPlugReportInstantUsageEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoElectricityClampCentralmeter)
    _LOGGER.info('→ Found %s Electricity Metering modules', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ElectricityClampCentralmeterReportInstantUsageEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericEnergyhome)
    _LOGGER.info('→ Found %s Energy Home\'s', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(
                Nhc2GenericEnergyhomeElectricalPowerProductionThresholdExceededEntity(device_instance, hub, gateway)
            )
            entities.append(Nhc2GenericEnergyhomeReportInstantUsageEntity(device_instance, hub, gateway))

        async_add_entities(entities)
