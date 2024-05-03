from homeassistant.components.sensor import SensorEntity

from ..nhccoco.devices.playerstatus_action import CocoPlayerstatusAction


class Nhc2PlayerstatusActionFeedbackMessageEntity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoPlayerstatusAction, hub, gateway):
        """Initialize a sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_feedback_message'
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

        self._attr_native_value = self._device.feedback_message

    @property
    def name(self) -> str:
        return 'Feedback Message'

    def on_change(self):
        self.schedule_update_ha_state()
