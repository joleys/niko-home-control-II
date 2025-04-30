from ..const import PROPERTY_BOOST, PROPERTY_BOOST_VALUE_FALSE, PROPERTY_BOOST_VALUE_TRUE, PROPERTY_CHARGING_MODE, \
    PROPERTY_CHARGING_STATUS, PROPERTY_COUPLING_STATUS, PROPERTY_ELECTRICAL_POWER, PROPERTY_EV_STATUS, \
    PROPERTY_NEXT_CHARGING_TIME, PROPERTY_REACHABLE_DISTANCE, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF, \
    PROPERTY_STATUS_VALUE_ON, PROPERTY_TARGET_DISTANCE, PROPERTY_TARGET_TIME, PROPERTY_TARGET_REACHED, \
    PROPERTY_TARGET_REACHED_VALUE_TRUE
from ..helpers import to_float_or_none, to_int_or_none
from .device import CoCoDevice


class CocoGenericChargingstation(CoCoDevice):
    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def is_status_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_ON

    @property
    def supports_status(self) -> bool:
        return self.has_property(PROPERTY_STATUS)

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
    def boost(self) -> str:
        return self.extract_property_value(PROPERTY_BOOST)

    @property
    def is_boost(self) -> bool:
        return self.boost == PROPERTY_BOOST_VALUE_TRUE

    @property
    def supports_boost(self) -> bool:
        return self.has_property(PROPERTY_BOOST)

    @property
    def target_distance(self) -> int | None:
        return to_int_or_none(self.extract_property_value(PROPERTY_TARGET_DISTANCE))

    @property
    def supports_target_distance(self) -> bool:
        return self.has_property(PROPERTY_TARGET_DISTANCE)

    @property
    def target_distance_range(self) -> tuple[float, float, float]:
        return self.extract_property_definition_description_range(PROPERTY_TARGET_DISTANCE)

    @property
    def target_time(self) -> str | None:
        return self.extract_property_value(PROPERTY_TARGET_TIME)

    @property
    def supports_target_time(self) -> bool:
        return self.has_property(PROPERTY_TARGET_TIME)

    @property
    def reachable_distance(self) -> str | None:
        return self.extract_property_value(PROPERTY_REACHABLE_DISTANCE)

    @property
    def supports_reachable_distance(self) -> bool:
        return self.has_property(PROPERTY_REACHABLE_DISTANCE)

    @property
    def reachable_distance_range(self) -> tuple[float, float, float]:
        return self.extract_property_definition_description_range(PROPERTY_REACHABLE_DISTANCE)

    @property
    def target_reached(self) -> str | None:
        return self.extract_property_value(PROPERTY_TARGET_REACHED)

    @property
    def is_target_reached(self) -> bool | None:
        return self.extract_property_value(PROPERTY_TARGET_REACHED) == PROPERTY_TARGET_REACHED_VALUE_TRUE

    @property
    def supports_target_reached(self) -> bool:
        return self.has_property(PROPERTY_TARGET_REACHED)

    @property
    def next_charging_time(self) -> str | None:
        return self.extract_property_value(PROPERTY_NEXT_CHARGING_TIME)

    @property
    def supports_next_charging_time(self) -> bool:
        return self.has_property(PROPERTY_NEXT_CHARGING_TIME)

    def turn_on(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON)

    def turn_off(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF)

    def set_charging_mode(self, gateway, charging_mode: str):
        gateway.add_device_control(self.uuid, PROPERTY_CHARGING_MODE, charging_mode)

    def set_boost(self, gateway, active: bool):
        if active:
            gateway.add_device_control(self.uuid, PROPERTY_BOOST, PROPERTY_BOOST_VALUE_TRUE)
        else:
            gateway.add_device_control(self.uuid, PROPERTY_BOOST, PROPERTY_BOOST_VALUE_FALSE)

    def set_target_distance(self, gateway, target_distance: int):
        gateway.add_device_control(self.uuid, PROPERTY_TARGET_DISTANCE, target_distance)

    def set_target_time(self, gateway, target_time: str):
        gateway.add_device_control(self.uuid, PROPERTY_TARGET_TIME, target_time)

    def set_reachable_distance(self, gateway, reachable_distance: int):
        gateway.add_device_control(self.uuid, PROPERTY_REACHABLE_DISTANCE, reachable_distance)

    def set_next_charging_time(self, gateway, next_charging_time: str):
        gateway.add_device_control(self.uuid, PROPERTY_NEXT_CHARGING_TIME, next_charging_time)
