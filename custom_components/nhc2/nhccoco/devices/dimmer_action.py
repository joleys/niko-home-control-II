from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON, PROPERTY_STATUS_VALUE_OFF, \
    PROPERTY_BRIGHTNESS, PROPERTY_ALIGNED, PROPERTY_ALIGNED_VALUE_TRUE
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoDimmerAction(CoCoDevice):
    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def status_brightness(self) -> int:
        return int(self.extract_property_value(PROPERTY_BRIGHTNESS))

    @property
    def status_aligned(self) -> str:
        return self.extract_property_value(PROPERTY_ALIGNED)

    @property
    def is_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_ON

    @property
    def is_aligned(self) -> bool:
        return self.status_aligned == PROPERTY_ALIGNED_VALUE_TRUE

    @property
    def support_brightness(self) -> bool:
        return True

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def turn_on(self, gateway):
        gateway._add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON)

    def turn_off(self, gateway):
        gateway._add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF)

    def set_brightness(self, gateway, brightness: int):
        gateway._add_device_control(self.uuid, PROPERTY_BRIGHTNESS, str(brightness))
