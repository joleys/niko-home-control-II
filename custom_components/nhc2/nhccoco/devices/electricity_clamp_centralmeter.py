from ..const import PROPERTY_ELECTRICAL_POWER, PROPERTY_ELECTRICAL_POWER1, PROPERTY_ELECTRICAL_POWER2, \
    PROPERTY_ELECTRICAL_POWER3, PROPERTY_REPORT_INSTANT_USAGE, PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE, \
    PARAMETER_FLOW, PARAMETER_SEGMENT, PARAMETER_CLAMP_TYPE, PARAMETER_INVERTED, PARAMETER_INVERTED1, \
    PARAMETER_INVERTED2, PARAMETER_INVERTED3, PARAMETER_INVERTED_VALUE_TRUE, PARAMETER_INVERTER_TYPE
from ..helpers import to_float_or_none
from .device import CoCoDevice


class CocoElectricityClampCentralmeter(CoCoDevice):
    @property
    def electrical_power(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER))

    @property
    def supports_electrical_power(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER)

    @property
    def electrical_power1(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER1))

    @property
    def supports_electrical_power1(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER1)

    @property
    def electrical_power2(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER2))

    @property
    def supports_electrical_power2(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER2)

    @property
    def electrical_power3(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER3))

    @property
    def supports_electrical_power3(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER3)

    @property
    def is_report_instant_usage(self) -> bool:
        return self.extract_property_value(PROPERTY_REPORT_INSTANT_USAGE) == PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE

    @property
    def inverter_type(self) -> str:
        return self.extract_parameter_value(PARAMETER_INVERTER_TYPE)

    @property
    def supports_inverter_type(self) -> bool:
        return self.has_parameter(PARAMETER_INVERTER_TYPE)

    @property
    def is_inverted(self) -> bool:
        return self.extract_parameter_value(PARAMETER_INVERTED) == PARAMETER_INVERTED_VALUE_TRUE

    @property
    def supports_inverted(self) -> bool:
        return self.has_parameter(PARAMETER_INVERTED)

    @property
    def is_inverted1(self) -> bool:
        return self.extract_parameter_value(PARAMETER_INVERTED1) == PARAMETER_INVERTED_VALUE_TRUE

    @property
    def supports_inverted1(self) -> bool:
        return self.has_parameter(PARAMETER_INVERTED1)

    @property
    def is_inverted2(self) -> bool:
        return self.extract_parameter_value(PARAMETER_INVERTED2) == PARAMETER_INVERTED_VALUE_TRUE

    @property
    def supports_inverted2(self) -> bool:
        return self.has_parameter(PARAMETER_INVERTED2)

    @property
    def is_inverted3(self) -> bool:
        return self.extract_parameter_value(PARAMETER_INVERTED3) == PARAMETER_INVERTED_VALUE_TRUE

    @property
    def supports_inverted3(self) -> bool:
        return self.has_parameter(PARAMETER_INVERTED3)

    @property
    def flow(self) -> str:
        return self.extract_parameter_value(PARAMETER_FLOW)

    @property
    def supports_flow(self) -> bool:
        return self.has_parameter(PARAMETER_FLOW)

    @property
    def segment(self) -> str:
        return self.extract_parameter_value(PARAMETER_SEGMENT)

    @property
    def supports_segment(self) -> bool:
        return self.has_parameter(PARAMETER_SEGMENT)

    @property
    def clamp_type(self) -> str:
        return self.extract_parameter_value(PARAMETER_CLAMP_TYPE)

    @property
    def supports_clamp_type(self) -> bool:
        return self.has_parameter(PARAMETER_CLAMP_TYPE)

    @property
    def is_online(self) -> bool:
        # For some reason NHC return `False` for these devices. Sor overruling this.
        return True

    def enable_report_instant_usage(self, gateway):
        gateway.add_device_control(
            self.uuid,
            PROPERTY_REPORT_INSTANT_USAGE,
            PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE
        )
