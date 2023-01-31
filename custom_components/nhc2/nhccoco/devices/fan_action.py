from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_FAN_SPEED

from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoFanAction(CoCoDevice):
    @property
    def fan_speed(self) -> str:
        return self.extract_property_value(PROPERTY_FAN_SPEED)

    @property
    def possible_fan_speeds(self) -> list[str]:
        self.extract_property_definition_description_choices(PROPERTY_FAN_SPEED)

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def set_fan_speed(self, gateway, speed: str):
        gateway.add_device_control(
            self.uuid,
            PROPERTY_FAN_SPEED,
            speed
        )
