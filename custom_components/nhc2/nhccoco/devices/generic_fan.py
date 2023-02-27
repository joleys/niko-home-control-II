from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_PROGRAM, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON, \
    PROPERTY_STATUS_VALUE_OFF, PROPERTY_FAN_SPEED, PROPERTY_BOOST, PROPERTY_BOOST_VALUE_TRUE, \
    PROPERTY_BOOST_VALUE_FALSE, PROPERTY_CO2, PROPERTY_HUMIDITY, PROPERTY_COUPLING_STATUS
from ..helpers import to_int_or_none
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoGenericFan(CoCoDevice):
    @property
    def program(self) -> str:
        return self.extract_property_value(PROPERTY_PROGRAM)

    @property
    def possible_programs(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_PROGRAM)

    @property
    def supports_program(self):
        return self.has_property(PROPERTY_PROGRAM)

    @property
    def fan_speed(self):
        if self.is_fan_speed_range:
            return to_int_or_none(self.extract_property_value(PROPERTY_FAN_SPEED))

        return self.extract_property_value(PROPERTY_FAN_SPEED)

    @property
    def possible_fan_speeds(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_FAN_SPEED)

    @property
    def supports_fan_speed(self) -> bool:
        return self.has_property(PROPERTY_FAN_SPEED)

    @property
    def fan_speed_range(self) -> tuple[float, float, float]:
        return self.extract_property_definition_description_range(PROPERTY_FAN_SPEED)

    @property
    def is_fan_speed_range(self) -> bool:
        return 'Range' in self.extract_property_definition(PROPERTY_FAN_SPEED)['Description']

    @property
    def boost(self) -> str:
        return self.extract_property_value(PROPERTY_BOOST)

    @property
    def is_boost(self) -> bool:
        return self.boost == PROPERTY_BOOST_VALUE_TRUE

    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def is_status_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_ON

    @property
    def co2(self) -> int:
        return to_int_or_none(self.extract_property_value(PROPERTY_CO2))

    @property
    def supports_co2(self) -> bool:
        return self.has_property(PROPERTY_CO2)

    @property
    def humidity(self) -> int:
        return to_int_or_none(self.extract_property_value(PROPERTY_HUMIDITY))

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

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def set_program(self, gateway, program: str):
        gateway.add_device_control(self.uuid, PROPERTY_PROGRAM, program)

    def set_fan_speed(self, gateway, fan_speed: str):
        gateway.add_device_control(self.uuid, PROPERTY_FAN_SPEED, fan_speed)

    def set_boost(self, gateway, boost: bool):
        if boost:
            gateway.add_device_control(self.uuid, PROPERTY_BOOST, PROPERTY_BOOST_VALUE_TRUE)
        else:
            gateway.add_device_control(self.uuid, PROPERTY_BOOST, PROPERTY_BOOST_VALUE_FALSE)

    def set_status(self, gateway, status: bool):
        if status:
            gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON)
        else:
            gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF)
