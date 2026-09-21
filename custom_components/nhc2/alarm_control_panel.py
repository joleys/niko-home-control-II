"""Support for NHC2 Alarm Control panel."""
import logging

from .nhccoco.coco import CoCo

from .entities.alarms_action_alarm_control_panel import Nhc2AlarmsActionAlarmControlPanelEntity
from .nhccoco.devices.alarms_action import CocoAlarmsAction

from .const import KEY_GATEWAY

from .hub import async_get_hub

KEY_ENTITY = 'nhc2_alarm_control_panels'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring alarm control panels')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = async_get_hub(hass, config_entry)

    device_instances = gateway.get_device_instances(CocoAlarmsAction)
    _LOGGER.info('→ Found %s NHC Basic Alarm Actions or NHC Panic Mode Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AlarmsActionAlarmControlPanelEntity(device_instance, hub, gateway))

        async_add_entities(entities)
