from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, AlarmControlPanelEntityFeature
from homeassistant.const import STATE_ALARM_DISARMED, STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMING

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.alarms_action import CocoAlarmsAction


class Nhc2AlarmsActionAlarmControlPanelEntity(AlarmControlPanelEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoAlarmsAction, hub, gateway):
        """Initialize a lock sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        self._attr_supported_features = AlarmControlPanelEntityFeature.ARM_AWAY

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': BRAND,
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def state(self) -> str:
        if self._device.is_off:
            return STATE_ALARM_DISARMED
        if self._device.is_on:
            return STATE_ALARM_ARMED_AWAY
        if self._device.is_intermediate:
            return STATE_ALARM_ARMING

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_alarm_arm_away(self, code=None) -> None:
        self._device.arm(self._gateway)
        self.on_change()

    async def async_alarm_disarm(self, code=None) -> None:
        self._device.disarm(self._gateway)
        self.on_change()

