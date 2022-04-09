from .coco_entity import CoCoEntity
from .coco_fan_speed import CoCoFanSpeed
from .const import KEY_FAN_SPEED
from .helpers import extract_property_value_from_device


class CoCoFan(CoCoEntity):

    @property
    def fan_speed(self) -> CoCoFanSpeed:
        return self._fan_speed

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._fan_speed = None
        self.update_dev(dev, callback_container)

    def change_speed(self, speed: CoCoFanSpeed):
        self._command_device_control(self._uuid, KEY_FAN_SPEED, speed.value)

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        status_value = extract_property_value_from_device(dev, KEY_FAN_SPEED)
        if status_value and self._fan_speed != CoCoFanSpeed(status_value):
            self._fan_speed = CoCoFanSpeed(status_value)
            has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()
