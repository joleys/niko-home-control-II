from ..const import PROPERTY_AMBIENT_TEMPERATURE
from ..helpers import to_float_or_none
from .device import CoCoDevice


class CocoGenericThermometer(CoCoDevice):
    @property
    def ambient_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_AMBIENT_TEMPERATURE))
