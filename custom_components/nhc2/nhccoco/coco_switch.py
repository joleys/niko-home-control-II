from .coco_entity import CoCoEntity
from .const import KEY_STATUS, VALUE_ON, VALUE_OFF
from .helpers import extract_property_value_from_device


class CoCoSwitch(CoCoEntity):

    @property
    def is_on(self):
        return self._is_on

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._is_on = None
        self.update_dev(dev, callback_container)

    def turn_on(self):
        self._command_device_control(self._uuid, KEY_STATUS, VALUE_ON)

    def turn_off(self):
        self._command_device_control(self._uuid, KEY_STATUS, VALUE_OFF)

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        status_value = extract_property_value_from_device(dev, KEY_STATUS)
        if status_value and self._is_on != (status_value == VALUE_ON):
            self._is_on = (status_value == VALUE_ON)
            has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()
