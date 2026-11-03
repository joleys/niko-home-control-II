from ..const import PROPERTY_FAN_SPEED, PROPERTY_AIR_QUALITY, PROPERTY_CO2, PROPERTY_HUMIDITY, \
    PROPERTY_COUPLING_STATUS, PROPERTY_FILTER_STATUS, PROPERTY_FILTER_STATUS_VALUE_CLEANING_NEEDED
from .device import CoCoDevice


class CocoFluxFan(CoCoDevice):
    @property
    def fan_speed(self) -> str:
        return self.extract_property_value(PROPERTY_FAN_SPEED)

    @property
    def possible_fan_speeds(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_FAN_SPEED)

    def set_fan_speed(self, gateway, fan_speed: str):
        gateway.add_device_control(self.uuid, PROPERTY_FAN_SPEED, fan_speed)

    @property
    def air_quality(self) -> str:
        return self.extract_property_value(PROPERTY_AIR_QUALITY)

    @property
    def possible_air_quality(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_AIR_QUALITY)

    @property
    def supports_air_quality(self) -> bool:
        return self.has_property(PROPERTY_AIR_QUALITY)

    @property
    def co2(self) -> str:
        return self.extract_property_value(PROPERTY_CO2)

    @property
    def possible_co2(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_CO2)

    @property
    def supports_co2(self) -> bool:
        return self.has_property(PROPERTY_CO2)

    @property
    def humidity(self) -> str:
        return self.extract_property_value(PROPERTY_HUMIDITY)

    @property
    def possible_humidity(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_HUMIDITY)

    @property
    def supports_humidity(self) -> bool:
        return self.has_property(PROPERTY_HUMIDITY)

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
    def filter_status(self) -> str:
        return self.extract_property_value(PROPERTY_FILTER_STATUS)

    @property
    def supports_filter_status(self) -> bool:
        return self.has_property(PROPERTY_FILTER_STATUS)

    @property
    def is_filter_cleaning_needed(self) -> bool:
        return self.filter_status == PROPERTY_FILTER_STATUS_VALUE_CLEANING_NEEDED
