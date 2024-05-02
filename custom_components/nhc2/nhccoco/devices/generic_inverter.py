from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_COUPLING_STATUS, PROPERTY_REPORT_INSTANT_USAGE, \
    PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE, PROPERTY_ELECTRICAL_POWER_PRODUCTION
from ..helpers import to_float_or_none

from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoGenericInverter(CoCoDevice):
    @property
    def coupling_status(self) -> str:
        return self.extract_property_value(PROPERTY_COUPLING_STATUS)

    @property
    def possible_coupling_status(self) -> list[str]:
        return self.extract_property_definition_description_choices(PROPERTY_COUPLING_STATUS)

    @property
    def supports_coupling_status(self) -> bool:
        return self.has_property(PROPERTY_COUPLING_STATUS) and self.coupling_status in self.possible_coupling_status

    @property
    def is_report_instant_usage(self) -> bool:
        return self.extract_property_value(PROPERTY_REPORT_INSTANT_USAGE) == PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE

    @property
    def electrical_power_production(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER_PRODUCTION))

    @property
    def supports_electrical_power_production(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER_PRODUCTION)

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def enable_report_instant_usage(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_REPORT_INSTANT_USAGE, PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE)
