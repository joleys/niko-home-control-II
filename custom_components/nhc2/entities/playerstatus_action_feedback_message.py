from homeassistant.components.sensor import SensorEntity

from ..nhccoco.devices.playerstatus_action import CocoPlayerstatusAction
from .nhc_entity import NHCBaseEntity


class Nhc2PlayerstatusActionFeedbackMessageEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoPlayerstatusAction, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_feedback_message'
        self._attr_native_value = self._device.feedback_message

    @property
    def name(self) -> str:
        return 'Feedback Message'
