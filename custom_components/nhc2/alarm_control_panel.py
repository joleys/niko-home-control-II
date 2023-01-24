"""Support for NHC2 Alarm Control panel."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.alarms_action_alarm_control_panel import Nhc2AlarmsActionAlarmControlPanelEntity
from .nhccoco.devices.alarms_action import CocoAlarmsAction

from .const import DOMAIN, KEY_GATEWAY

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_alarm_control_panels'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring alarm control panels')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoAlarmsAction)
    _LOGGER.info('→ Found %s basic alarms', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AlarmsActionAlarmControlPanelEntity(device_instance, hub, gateway))

        async_add_entities(entities)
