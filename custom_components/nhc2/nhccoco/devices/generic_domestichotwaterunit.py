from ..const import PROPERTY_BOOST, PROPERTY_BOOST_VALUE_FALSE, PROPERTY_BOOST_VALUE_TRUE, PROPERTY_COUPLING_STATUS, \
    PROPERTY_DOMESTIC_HOT_WATER_TEMPERATURE, PROPERTY_PROGRAM
from ..helpers import to_float_or_none
from .device import CoCoDevice


class CocoGenericDomestichotwaterunit(CoCoDevice):
    @property
    def domestic_hot_water_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_DOMESTIC_HOT_WATER_TEMPERATURE))

    @property
    def domestic_hot_water_temperature_range(self) -> tuple[float, float, float]:
        return self.extract_property_definition_description_range(PROPERTY_DOMESTIC_HOT_WATER_TEMPERATURE)

    @property
    def program(self) -> str:
        return self.extract_property_value(PROPERTY_PROGRAM)

    @property
    def possible_programs(self) -> list[str]:
        return self.extract_property_definition_description_choices(PROPERTY_PROGRAM)

    @property
    def supports_program(self) -> bool:
        return self.has_property(PROPERTY_PROGRAM)

    @property
    def boost(self) -> str:
        return self.extract_property_value(PROPERTY_BOOST)

    @property
    def is_boost(self) -> bool:
        return self.boost == PROPERTY_BOOST_VALUE_TRUE

    @property
    def coupling_status(self) -> str:
        return self.extract_property_value(PROPERTY_COUPLING_STATUS)

    @property
    def possible_coupling_status(self) -> list[str]:
        return self.extract_property_definition_description_choices(PROPERTY_COUPLING_STATUS)

    @property
    def supports_coupling_status(self) -> bool:
        return self.has_property(PROPERTY_COUPLING_STATUS) and self.coupling_status in self.possible_coupling_status

    def set_domestic_hot_water_temperature(self, gateway, temperature: float):
        gateway.add_device_control(self.uuid, PROPERTY_DOMESTIC_HOT_WATER_TEMPERATURE, str(temperature))

    def set_program(self, gateway, program: str):
        gateway.add_device_control(self.uuid, PROPERTY_PROGRAM, program)

    def set_boost(self, gateway, active: bool):
        if active:
            gateway.add_device_control(self.uuid, PROPERTY_BOOST, PROPERTY_BOOST_VALUE_TRUE)
        else:
            gateway.add_device_control(self.uuid, PROPERTY_BOOST, PROPERTY_BOOST_VALUE_FALSE)
