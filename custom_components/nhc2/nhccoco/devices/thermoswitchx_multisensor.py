from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_HEAT_INDEX, PROPERTY_AMBIENT_TEMPERATURE, PROPERTY_HUMIDITY

from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoThermoswitchxMultisensor(CoCoDevice):
    @property
    def heat_index(self) -> int:
        return self.extract_property_value(PROPERTY_HEAT_INDEX)

    @property
    def supports_heat_index(self) -> bool:
        return self.has_property(PROPERTY_HEAT_INDEX)

    @property
    def ambient_temperature(self) -> float:
        return self.extract_property_value(PROPERTY_AMBIENT_TEMPERATURE)

    @property
    def supports_ambient_temperature(self) -> bool:
        return self.has_property(PROPERTY_AMBIENT_TEMPERATURE)

    @property
    def humidity(self) -> float:
        return self.extract_property_value(PROPERTY_HUMIDITY)

    @property
    def supports_humidity(self) -> bool:
        return self.has_property(PROPERTY_HUMIDITY)

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()
