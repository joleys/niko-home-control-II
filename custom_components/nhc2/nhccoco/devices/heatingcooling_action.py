from ..const import PROPERTY_HEATING_MODE, PROPERTY_HEATING_MODE_VALUE_TRUE, PROPERTY_COOLING_MODE, \
    PROPERTY_COOLING_MODE_VALUE_TRUE
from .device import CoCoDevice


class CocoHeatingcoolingAction(CoCoDevice):
    @property
    def heating_mode(self) -> str:
        return self.extract_property_value(PROPERTY_HEATING_MODE)

    @property
    def is_heating_mode(self) -> bool:
        return self.heating_mode == PROPERTY_HEATING_MODE_VALUE_TRUE

    @property
    def cooling_mode(self) -> str:
        return self.extract_property_value(PROPERTY_COOLING_MODE)

    @property
    def is_cooling_mode(self) -> bool:
        return self.cooling_mode == PROPERTY_COOLING_MODE_VALUE_TRUE
