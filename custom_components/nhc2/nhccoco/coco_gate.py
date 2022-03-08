from .coco_entity import CoCoEntity
from .const import KEY_BASICSTATE, KEY_POSITION, VALUE_OPEN, VALUE_STOP, VALUE_CLOSE, VALUE_TRIGGERED
from .helpers import extract_property_value_from_device

class CoCoGate(CoCoEntity):

    @property
    def position(self):
        return self._position

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._position = None
        self.update_dev(dev, callback_container)

    def open(self):
        if self._state == VALUE_CLOSE:
            self._command_device_control(self._uuid, KEY_BASICSTATE, VALUE_TRIGGERED)

    def stop(self):
        self._command_device_control(self._uuid, KEY_BASICSTATE, VALUE_TRIGGERED)

    def close(self):
        if self._state == VALUE_OPEN:
            self._command_device_control(self._uuid, KEY_BASICSTATE, VALUE_TRIGGERED)

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        position_value = extract_property_value_from_device(dev, KEY_BASICSTATE)
        if position_value is not None and self._position != position_value:
            self._position = position_value
            has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()
