from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_ACTIVE, PROPERTY_ACTIVE_VALUE_TRUE

from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoTimescheduleAction(CoCoDevice):
    @property
    def active(self) -> str:
        return self.extract_property_value(PROPERTY_ACTIVE)

    @property
    def is_active(self) -> bool:
        return self.active == PROPERTY_ACTIVE_VALUE_TRUE

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()
