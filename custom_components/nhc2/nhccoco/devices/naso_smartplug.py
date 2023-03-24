from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_ELECTRICAL_POWER, PROPERTY_REPORT_INSTANT_USAGE, \
    PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE, PARAMETER_FEEDBACK_ENABLED, PARAMETER_FEEDBACK_ENABLED_VALUE_TRUE, \
    PARAMETER_MEASURING_ONLY, PARAMETER_MEASURING_ONLY_VALUE_TRUE
from ..helpers import to_float_or_none
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoNasoSmartplug(CoCoDevice):
    @property
    def electrical_power(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER))

    @property
    def is_report_instant_usage(self) -> bool:
        return self.extract_property_value(PROPERTY_REPORT_INSTANT_USAGE) == PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE

    @property
    def is_feedback_enabled(self) -> bool:
        return self.extract_parameter_value(PARAMETER_FEEDBACK_ENABLED) == PARAMETER_FEEDBACK_ENABLED_VALUE_TRUE

    @property
    def is_measuring_only(self) -> bool:
        return self.extract_parameter_value(PARAMETER_MEASURING_ONLY) == PARAMETER_MEASURING_ONLY_VALUE_TRUE

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def enable_report_instant_usage(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_REPORT_INSTANT_USAGE, PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE)
