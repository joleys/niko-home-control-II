from ..const import PARAMETER_AMBIENT_TEMPERATURE_REPORTING, PARAMETER_AMBIENT_TEMPERATURE_REPORTING_DISABLED, \
    PARAMETER_HEAT_INDEX_REPORTING, PARAMETER_HEAT_INDEX_REPORTING_DISABLED, PARAMETER_HUMIDITY_REPORTING, \
    PARAMETER_HUMIDITY_REPORTING_DISABLED, PROPERTY_HEAT_INDEX, PROPERTY_AMBIENT_TEMPERATURE, PROPERTY_HUMIDITY
from ..helpers import to_float_or_none, to_int_or_none
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoThermoswitchxMultisensor(CoCoDevice):
    @property
    def heat_index(self) -> int:
        return to_int_or_none(self.extract_property_value(PROPERTY_HEAT_INDEX))

    @property
    def supports_heat_index(self) -> bool:
        if (self.has_parameter(PARAMETER_HEAT_INDEX_REPORTING) and self.extract_parameter_value(
                PARAMETER_HEAT_INDEX_REPORTING) == PARAMETER_HEAT_INDEX_REPORTING_DISABLED):
            _LOGGER.debug(f'{self.name} does not support heat index, as reporting is disabled.')
            return False
        return self.has_property(PROPERTY_HEAT_INDEX)

    @property
    def ambient_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_AMBIENT_TEMPERATURE))

    @property
    def supports_ambient_temperature(self) -> bool:
        if self.has_parameter(PARAMETER_AMBIENT_TEMPERATURE_REPORTING) and self.extract_parameter_value(
                PARAMETER_AMBIENT_TEMPERATURE_REPORTING) == PARAMETER_AMBIENT_TEMPERATURE_REPORTING_DISABLED:
            _LOGGER.debug(f'{self.name} does not support ambient temperature, as reporting is disabled.')
            return False
        return self.has_property(PROPERTY_AMBIENT_TEMPERATURE)

    @property
    def humidity(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_HUMIDITY))

    @property
    def supports_humidity(self) -> bool:
        if self.has_parameter(PARAMETER_HUMIDITY_REPORTING) and self.extract_parameter_value(
                PARAMETER_HUMIDITY_REPORTING) == PARAMETER_HUMIDITY_REPORTING_DISABLED:
            _LOGGER.debug(f'{self.name} does not support humidity, as reporting is disabled.')
            return False

        return self.has_property(PROPERTY_HUMIDITY)
