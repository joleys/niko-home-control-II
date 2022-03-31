from .coco_entity import CoCoEntity
from .const import KEY_BASICSTATE, KEY_POSITION, GATE_VALUE_OPEN, GATE_VALUE_CLOSE, GATE_VALUE_TRIGGERED, \
                   GATE_MOVING, VALUE_OPEN, VALUE_STOP, VALUE_CLOSE, KEY_ACTION
from ..const import GARAGE_DOOR
from .helpers import extract_property_value_from_device

import logging
_LOGGER = logging.getLogger(__name__)

class CoCoCover(CoCoEntity):

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._position = None
        self._state = None
        self._status = None
        self._model = super().model
        self.update_dev(dev, callback_container)

    @property
    def position(self):
        return self._position

    @property
    def state(self):
        return self._state

    def open(self):
        if self._model == GARAGE_DOOR:
            if self._status == GATE_VALUE_CLOSE:
                _LOGGER.debug('command: OPEN')
                self._command_device_control(self._uuid, KEY_BASICSTATE, GATE_VALUE_TRIGGERED)
        else:
            self._command_device_control(self._uuid, KEY_ACTION, VALUE_OPEN)

    def stop(self):
        if self._model == GARAGE_DOOR:
            _LOGGER.debug('command: STOP')
            self._command_device_control(self._uuid, KEY_BASICSTATE, GATE_VALUE_TRIGGERED)
        else:
            self._command_device_control(self._uuid, KEY_ACTION, VALUE_STOP)

    def close(self):
        if self._model == GARAGE_DOOR:
            if self._status == GATE_VALUE_OPEN:
                _LOGGER.debug('command: CLOSE')
                self._command_device_control(self._uuid, KEY_BASICSTATE, GATE_VALUE_TRIGGERED)
        else:
            self._command_device_control(self._uuid, KEY_ACTION, VALUE_CLOSE)

    def set_position(self, position: int):
        self._command_device_control(self._uuid, KEY_POSITION, str(position))

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        state_value = extract_property_value_from_device(dev, KEY_BASICSTATE)
        if state_value is not None and self._status != state_value:
            if self._status == GATE_VALUE_CLOSE and state_value == GATE_MOVING:
                self._state = 'OPENING'
            elif self._status == GATE_VALUE_OPEN and state_value == GATE_MOVING:
                self._state = 'CLOSING'
            elif state_value == GATE_VALUE_CLOSE:
                self._state = 'CLOSED'
            elif state_value == GATE_VALUE_OPEN:
                self._state = 'OPEN'
            self._status = state_value
            has_changed = True
        position_value = extract_property_value_from_device(dev, KEY_POSITION)
        if position_value is not None and self._position != int(position_value):
            self._position = int(position_value)
            has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()

