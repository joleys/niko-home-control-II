from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, AlarmControlPanelEntityFeature, \
  AlarmControlPanelState

from ..nhccoco.devices.alarms_action import CocoAlarmsAction
from .nhc_entity import NHCBaseEntity


class Nhc2AlarmsActionAlarmControlPanelEntity(NHCBaseEntity, AlarmControlPanelEntity):
    _attr_has_entity_name = True
    _attr_name = None
    _attr_code_arm_required = False

    def __init__(self, device_instance: CocoAlarmsAction, hub, gateway):
        """Initialize a alarm lock panel."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

        self._attr_supported_features = AlarmControlPanelEntityFeature.ARM_AWAY

    @property
    def alarm_state(self) -> str:
        if self._device.is_basic_state_off:
            return AlarmControlPanelState.DISARMED
        if self._device.is_basic_state_on:
            return AlarmControlPanelState.ARMED_AWAY
        if self._device.is_basic_state_intermediate:
            return AlarmControlPanelState.ARMING

    async def async_alarm_arm_away(self, code=None) -> None:
        self._device.arm(self._gateway)
        self.schedule_update_ha_state()

    async def async_alarm_disarm(self, code=None) -> None:
        self._device.disarm(self._gateway)
        self.schedule_update_ha_state()
