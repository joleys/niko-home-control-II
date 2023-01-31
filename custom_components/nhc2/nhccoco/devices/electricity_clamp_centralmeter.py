from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_ELECTRICAL_POWER, PROPERTY_REPORT_INSTANT_USAGE, \
    PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE, PARAMETER_FLOW, PARAMETER_SEGMENT, PARAMETER_CLAMP_TYPE
from ..helpers import to_float_or_none
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoElectricityClampCentralmeter(CoCoDevice):
    @property
    def electrical_power(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER))

    @property
    def is_report_instant_usage(self) -> bool:
        return self.extract_property_value(PROPERTY_REPORT_INSTANT_USAGE) == PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE

    @property
    def flow(self) -> str:
        return self.extract_parameter_value(PARAMETER_FLOW)

    @property
    def possible_flows(self) -> list:
        self.extract_property_definition_description_choices(PARAMETER_FLOW)

    @property
    def segment(self) -> str:
        return self.extract_parameter_value(PARAMETER_SEGMENT)

    @property
    def possible_segments(self) -> list:
        self.extract_property_definition_description_choices(PARAMETER_SEGMENT)

    @property
    def clamp_type(self) -> str:
        return self.extract_parameter_value(PARAMETER_CLAMP_TYPE)

    @property
    def possible_clamp_types(self) -> list:
        self.extract_property_definition_description_choices(PARAMETER_CLAMP_TYPE)

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def enable_report_instant_usage(self, gateway):
        gateway.add_device_control(
            self.uuid,
            PROPERTY_REPORT_INSTANT_USAGE,
            PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE
        )
