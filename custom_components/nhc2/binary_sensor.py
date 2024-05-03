import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.accesscontrol_action_call_answered import Nhc2AccesscontrolActionCallAnsweredEntity
from .entities.accesscontrol_action_call_pending import Nhc2AccesscontrolActionCallPendingEntity
from .entities.accesscontrol_action_decline_call_applied_on_all_devices import \
    Nhc2AccesscontrolActionDeclineCallAppliedOnAllDevicesEntity
from .entities.alloff_action_active import Nhc2AlloffActionActiveEntity
from .entities.alloff_action_basicstate import Nhc2AlloffActionBasicStateEntity
from .entities.alloff_action_started import Nhc2AlloffActionStartedEntity
from .entities.audiocontrol_action_connected import Nhc2AudiocontrolActionConnectedEntity
from .entities.audiocontrol_action_title_aligned import Nhc2AudiocontrolActionTitleAlignedEntity
from .entities.audiocontrol_action_volume_aligned import Nhc2AudiocontrolActionVolumeAlignedEntity
from .entities.bellbutton_action_decline_call_applied_on_all_devices import \
    Nhc2BellbuttonActionDeclineCallAppliedOnAllDevicesEntity
from .entities.comfort_action_all_started import Nhc2ComfortActionAllStartedEntity
from .entities.comfort_action_basicstate import Nhc2ComfortActionBasicStateEntity
from .entities.comfort_action_mood_active import Nhc2ComfortActionMoodActiveEntity
from .entities.dimmer_action_aligned import Nhc2DimmerActionAlignedEntity
from .entities.electricalheating_action_basicstate import Nhc2ElectricalheatingActionBasicStateEntity
from .entities.electricity_clamp_centralmeter_report_instant_usage import \
    Nhc2ElectricityClampCentralmeterReportInstantUsageEntity
from .entities.garagedoor_action_port_closed import Nhc2GaragedoorActionPortClosedEntity
from .entities.generic_action_all_started import Nhc2GenericActionAllStartedEntity
from .entities.generic_action_start_active import Nhc2GenericActionStartActiveEntity
from .entities.generic_energyhome_electrical_power_production_threshold_exceeded import \
    Nhc2GenericEnergyhomeElectricalPowerProductionThresholdExceededEntity
from .entities.generic_energyhome_report_instant_usage import Nhc2GenericEnergyhomeReportInstantUsageEntity
from .entities.generic_inverter_report_instant_usage import Nhc2GenericInverterReportInstantUsageEntity
from .entities.generic_smartplug_report_instant_usage import Nhc2GenericSmartplugReportInstantUsageEntity
from .entities.heatingcooling_action_cooling_mode import Nhc2HeatingcoolingActionCoolingModeEntity
from .entities.heatingcooling_action_heating_mode import Nhc2HeatingcoolingActionHeatingModeEntity
from .entities.hvacthermostat_hvac_hvac_on import Nhc2HvacthermostatHvacHvacOnEntity
from .entities.motor_action_aligned import Nhc2MotorActionAlignedEntity
from .entities.motor_action_moving import Nhc2MotorActionMovingEntity
from .entities.naso_smartplug_feedback_enabled import Nhc2NasoSmartplugFeedbackEnabledEntity
from .entities.naso_smartplug_measuring_only import Nhc2NasoSmartplugMeasuringOnlyEntity
from .entities.naso_smartplug_report_instant_usage import Nhc2NasoSmartplugReportInstantUsageEntity
from .entities.overallcomfort_action_start_active import Nhc2OverallcomfortActionStartActiveEntity
from .entities.overallcomfort_action_all_started import Nhc2OverallcomfortActionAllStartedEntity
from .entities.playerstatus_action_basicstate import Nhc2PlayerstatusActionBasicStateEntity
from .entities.timeschedule_action_active import Nhc2TimeschedulActionActiveEntity
from .nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction
from .nhccoco.devices.alloff_action import CocoAlloffAction
from .nhccoco.devices.audiocontrol_action import CocoAudiocontrolAction
from .nhccoco.devices.bellbutton_action import CocoBellbuttonAction
from .nhccoco.devices.comfort_action import CocoComfortAction
from .nhccoco.devices.dimmer_action import CocoDimmerAction
from .nhccoco.devices.electricalheating_action import CocoElectricalheatingAction
from .nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .nhccoco.devices.garagedoor_action import CocoGaragedoorAction
from .nhccoco.devices.gate_action import CocoGateAction
from .nhccoco.devices.generic_action import CocoGenericAction
from .nhccoco.devices.generic_energyhome import CocoGenericEnergyhome
from .nhccoco.devices.generic_inverter import CocoGenericInverter
from .nhccoco.devices.generic_smartplug import CocoGenericSmartplug
from .nhccoco.devices.heatingcooling_action import CocoHeatingcoolingAction
from .nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhccoco.devices.naso_smartplug import CocoNasoSmartplug
from .nhccoco.devices.overallcomfort_action import CocoOverallcomfortAction
from .nhccoco.devices.playerstatus_action import CocoPlayerstatusAction
from .nhccoco.devices.rolldownshutter_action import CocoRolldownshutterAction
from .nhccoco.devices.sunblind_action import CocoSunblindAction
from .nhccoco.devices.timeschedule_action import CocoTimescheduleAction
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
    _LOGGER.info('→ Found %s NHC Access Control Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AccesscontrolActionDeclineCallAppliedOnAllDevicesEntity(device_instance, hub, gateway))
            if device_instance.supports_call_answered:
                entities.append(Nhc2AccesscontrolActionCallAnsweredEntity(device_instance, hub, gateway))
            if device_instance.supports_call_pending:
                entities.append(Nhc2AccesscontrolActionCallPendingEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoAlloffAction)
    _LOGGER.info('→ Found %s NHC All Off Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AlloffActionActiveEntity(device_instance, hub, gateway))
            entities.append(Nhc2AlloffActionBasicStateEntity(device_instance, hub, gateway))

            if device_instance.supports_all_started:
                entities.append(Nhc2AlloffActionStartedEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoAudiocontrolAction)
    _LOGGER.info('→ Found %s NHC Audio Control Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AudiocontrolActionConnectedEntity(device_instance, hub, gateway))
            entities.append(Nhc2AudiocontrolActionVolumeAlignedEntity(device_instance, hub, gateway))
            entities.append(Nhc2AudiocontrolActionTitleAlignedEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoBellbuttonAction)
    _LOGGER.info('→ Found %s NHC BellButton Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2BellbuttonActionDeclineCallAppliedOnAllDevicesEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoDimmerAction)
    _LOGGER.info('→ Found %s NHC Dimmer Actions', len(device_instances))
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
            entities.append(Nhc2GenericActionStartActiveEntity(device_instance, hub, gateway))

            if device_instance.supports_all_started:
                entities.append(Nhc2GenericActionAllStartedEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGaragedoorAction)
    _LOGGER.info('→ Found %s NHC Garage Door Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            if device_instance.supports_port_closed:
                entities.append(Nhc2GaragedoorActionPortClosedEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoOverallcomfortAction)
    _LOGGER.info('→ Found %s NHC House Mode Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2OverallcomfortActionStartActiveEntity(device_instance, hub, gateway))

            if device_instance.supports_all_started:
                entities.append(Nhc2OverallcomfortActionAllStartedEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoHvacthermostatHvac)
    _LOGGER.info('→ Found %s NHC HVAC Thermostats', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2HvacthermostatHvacHvacOnEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoComfortAction)
    _LOGGER.info('→ Found %s NHC Mood Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ComfortActionBasicStateEntity(device_instance, hub, gateway))
            entities.append(Nhc2ComfortActionMoodActiveEntity(device_instance, hub, gateway))

            if device_instance.supports_all_started:
                entities.append(Nhc2ComfortActionAllStartedEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGateAction)
    device_instances += gateway.get_device_instances(CocoRolldownshutterAction)
    device_instances += gateway.get_device_instances(CocoSunblindAction)
    device_instances += gateway.get_device_instances(CocoVenetianblindAction)
    _LOGGER.info('→ Found %s NHC Motor Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2MotorActionMovingEntity(device_instance, hub, gateway))
            entities.append(Nhc2MotorActionAlignedEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoNasoSmartplug)
    _LOGGER.info('→ Found %s NHC Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2NasoSmartplugReportInstantUsageEntity(device_instance, hub, gateway))
            entities.append(Nhc2NasoSmartplugFeedbackEnabledEntity(device_instance, hub, gateway))
            entities.append(Nhc2NasoSmartplugMeasuringOnlyEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericSmartplug)
    _LOGGER.info('→ Found %s Generic Zigbee Smart plugs', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2GenericSmartplugReportInstantUsageEntity(device_instance, hub, gateway))

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

    device_instances = gateway.get_device_instances(CocoTimescheduleAction)
    _LOGGER.info('→ Found %s Timeschedule Actions (undocumented)', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2TimeschedulActionActiveEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoHeatingcoolingAction)
    _LOGGER.info('→ Found %s Heating Cooling Actions (undocumented)', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2HeatingcoolingActionCoolingModeEntity(device_instance, hub, gateway))
            entities.append(Nhc2HeatingcoolingActionHeatingModeEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoElectricalheatingAction)
    _LOGGER.info('→ Found %s Electricalheating Actions (undocumented)', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2ElectricalheatingActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoPlayerstatusAction)
    _LOGGER.info('→ Found %s NHC Player status action', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2PlayerstatusActionBasicStateEntity(device_instance, hub, gateway))

        async_add_entities(entities)

    device_instances = gateway.get_device_instances(CocoGenericInverter)
    _LOGGER.info('→ Found %s Generic Inverter Implementations (undocumented)', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            if device_instance.supports_coupling_status:
                entities.append(Nhc2GenericInverterReportInstantUsageEntity(device_instance, hub, gateway))

        async_add_entities(entities)
