from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from ..nhccoco.devices.velux_action import CocoVeluxAction
from .nhc_entity import NHCBaseEntity


class Nhc2VeluxActionFeedbackEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoVeluxAction, hub, gateway):
        """Initialize a enum sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_feedback'

        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = self._device.possible_feedback
        self._attr_native_value = self._device.feedback

    @property
    def name(self) -> str:
        return 'Feedback'

    @property
    def state(self) -> str:
        return self._device.feedback
