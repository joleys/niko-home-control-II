import logging

from .coco_entity import CoCoEntity
from .const import KEY_BASICSTATE, GATE_VALUE_OPEN, GATE_VALUE_CLOSE, GATE_VALUE_TRIGGERED, GATE_MOVING
from .helpers import extract_property_value_from_device

_LOGGER = logging.getLogger(__name__)

class CoCoGaragedoor(CoCoEntity):

    @property
    def position(self):
        return self._position

    @property
    def status(self):
        return self._state

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._position = None
        self._state = None
        self.update_dev(dev, callback_container)

    def open(self):
        if self._position == GATE_VALUE_CLOSE:
            self._command_device_control(self._uuid, KEY_BASICSTATE, GATE_VALUE_TRIGGERED)

    def stop(self):
        self._command_device_control(self._uuid, KEY_BASICSTATE, GATE_VALUE_TRIGGERED)

    def close(self):
        if self._position == GATE_VALUE_OPEN:
            self._command_device_control(self._uuid, KEY_BASICSTATE, GATE_VALUE_TRIGGERED)

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        position_value = extract_property_value_from_device(dev, KEY_BASICSTATE)
        if position_value is not None and self._position != position_value:
            if self._position == GATE_VALUE_CLOSE and position_value == GATE_MOVING:
                self._state = 'OPENING'
            elif self._position == GATE_VALUE_OPEN and position_value == GATE_MOVING:
                self._state = 'CLOSING'
            elif position_value == GATE_VALUE_CLOSE:
                self._state = 'CLOSED'
            elif position_value == GATE_VALUE_OPEN:
                self._state = 'OPEN'
            self._position = position_value
            has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()
