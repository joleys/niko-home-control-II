from ..const import PROPERTY_CHARGING_MODE, PROPERTY_CHARGING_STATUS, PROPERTY_COUPLING_STATUS, \
    PROPERTY_ELECTRICAL_POWER, PROPERTY_EV_STATUS, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF, PROPERTY_STATUS_VALUE_ON
from ..helpers import to_float_or_none
from .device import CoCoDevice


class CocoEaseeChargingstation(CoCoDevice):
    @property
    def supports_status(self) -> bool:
        return self.has_property(PROPERTY_STATUS)

    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def is_status_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_ON

    @property
    def charging_mode(self) -> str:
        return self.extract_property_value(PROPERTY_CHARGING_MODE)

    @property
    def possible_charging_modes(self) -> list[str]:
        return self.extract_property_definition_description_choices(PROPERTY_CHARGING_MODE)

    @property
    def supports_charging_mode(self) -> bool:
        return self.has_property(PROPERTY_CHARGING_MODE)

    @property
    def charging_status(self) -> str:
        return self.extract_property_value(PROPERTY_CHARGING_STATUS)

    @property
    def possible_charging_status(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_CHARGING_STATUS)

    @property
    def supports_charging_status(self) -> bool:
        return self.has_property(PROPERTY_CHARGING_STATUS)

    @property
    def coupling_status(self) -> str:
        return self.extract_property_value(PROPERTY_COUPLING_STATUS)

    @property
    def possible_coupling_status(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_COUPLING_STATUS)

    @property
    def supports_coupling_status(self) -> bool:
        return self.has_property(PROPERTY_COUPLING_STATUS)

    @property
    def ev_status(self) -> str:
        return self.extract_property_value(PROPERTY_EV_STATUS)

    @property
    def possible_ev_status(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_EV_STATUS)

    @property
    def supports_ev_status(self) -> bool:
        return self.has_property(PROPERTY_EV_STATUS)

    @property
    def electrical_power(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER))

    @property
    def supports_electrical_power(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER)

    def turn_on(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON)

    def turn_off(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF)

    def set_charging_mode(self, gateway, charging_mode: str):
        gateway.add_device_control(self.uuid, PROPERTY_CHARGING_MODE, charging_mode)
