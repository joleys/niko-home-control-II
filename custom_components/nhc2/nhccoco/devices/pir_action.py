from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_ON, \
    PROPERTY_BASIC_STATE_VALUE_TRIGGERED

from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoPirAction(CoCoDevice):
    @property
    def basic_state(self) -> str:
        return self.extract_property_value(PROPERTY_BASIC_STATE)

    @property
    def is_basic_state_on(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_ON

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def press(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_TRIGGERED)
