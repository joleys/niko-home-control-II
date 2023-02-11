from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_HEATING_MODE, PROPERTY_HEATING_MODE_VALUE_TRUE, \
    PROPERTY_COOLING_MODE, PROPERTY_COOLING_MODE_VALUE_TRUE
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoHeatingcoolingAction(CoCoDevice):
    @property
    def heating_mode(self) -> str:
        return self.extract_property_value(PROPERTY_HEATING_MODE)

    @property
    def is_heating_mode(self) -> bool:
        return self.heating_mode == PROPERTY_HEATING_MODE_VALUE_TRUE

    @property
    def cooling_mode(self) -> str:
        return self.extract_property_value(PROPERTY_COOLING_MODE)

    @property
    def is_cooling_mode(self) -> bool:
        return self.cooling_mode == PROPERTY_COOLING_MODE_VALUE_TRUE

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()
