from .coco_entity import CoCoEntity
from .const import KEY_FAN_SPEED
from .helpers import extract_property_value_from_device, extract_property_definitions


class CoCoFan(CoCoEntity):

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._fan_speed = None
        self.update_dev(dev, callback_container)

        self.get_fanspeed_params(dev)

    @property
    def fan_speed(self):
        return self._fan_speed

    @property
    def fan_speeds(self):
        return self._fan_speeds

    def change_speed(self, speed):
        self._command_device_control(self._uuid, KEY_FAN_SPEED, speed)
    
    def get_fanspeed_params(self, dev):
        """Get parameters for programs"""
        if dev and 'PropertyDefinitions' in dev:
            params = extract_property_definitions(dev, 'FanSpeed')['Description']
            values = params.split("(")[1].split(")")[0].split(",")
            self._fan_speeds = values

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        status_value = extract_property_value_from_device(dev, KEY_FAN_SPEED)
        if status_value and self._fan_speed != status_value:
            self._fan_speed = status_value
            has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()
