from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, AlarmControlPanelEntityFeature
from homeassistant.const import STATE_ALARM_DISARMED, STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMING

from ..nhccoco.devices.alarms_action import CocoAlarmsAction
from .nhc_entity import NHCBaseEntity


class Nhc2AlarmsActionAlarmControlPanelEntity(NHCBaseEntity, AlarmControlPanelEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoAlarmsAction, hub, gateway):
        """Initialize a lock sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_supported_features = AlarmControlPanelEntityFeature.ARM_AWAY

    @property
    def state(self) -> str:
        if self._device.is_basic_state_off:
            return STATE_ALARM_DISARMED
        if self._device.is_basic_state_on:
            return STATE_ALARM_ARMED_AWAY
        if self._device.is_basic_state_intermediate:
            return STATE_ALARM_ARMING

    async def async_alarm_arm_away(self, code=None) -> None:
        self._device.arm(self._gateway)
        self.schedule_update_ha_state()

    async def async_alarm_disarm(self, code=None) -> None:
        self._device.disarm(self._gateway)
        self.schedule_update_ha_state()
