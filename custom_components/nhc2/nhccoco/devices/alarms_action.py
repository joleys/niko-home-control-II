from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_ON, \
    PROPERTY_BASIC_STATE_VALUE_OFF, PROPERTY_BASIC_STATE_VALUE_INTERMEDIATE, PROPERTY_BASIC_STATE_VALUE_TRIGGERED
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoAlarmsAction(CoCoDevice):
    @property
    def basic_state(self) -> str:
        return self.extract_property_value(PROPERTY_BASIC_STATE)

    @property
    def possible_basic_states(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_BASIC_STATE)

    @property
    def is_basic_state_intermediate(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_INTERMEDIATE

    @property
    def is_basic_state_on(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_ON

    @property
    def is_basic_state_off(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_OFF

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def arm(self, gateway):
        if self.is_basic_state_on:
            return

        gateway.add_device_control(
            self.uuid,
            PROPERTY_BASIC_STATE,
            PROPERTY_BASIC_STATE_VALUE_TRIGGERED
        )

    def disarm(self, gateway):
        if self.is_basic_state_off:
            return

        gateway.add_device_control(
            self.uuid,
            PROPERTY_BASIC_STATE,
            PROPERTY_BASIC_STATE_VALUE_TRIGGERED
        )
