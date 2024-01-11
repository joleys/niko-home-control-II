from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_PROGRAM, PROPERTY_AMBIENT_TEMPERATURE, \
    PROPERTY_SETPOINT_TEMPERATURE, PROPERTY_OVERRULE_ACTIVE, PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE, \
    PROPERTY_OVERRULE_ACTIVE_VALUE_FALSE, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON, PROPERTY_STATUS_VALUE_OFF, \
    PROPERTY_OUTDOOR_TEMPERATURE, PROPERTY_OPERATION_MODE, PROPERTY_FAN_SPEED, PROPERTY_COUPLING_STATUS
from ..helpers import to_float_or_none
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoGenericHvac(CoCoDevice):
    @property
    def setpoint_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_SETPOINT_TEMPERATURE))

    @property
    def ambient_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_AMBIENT_TEMPERATURE))

    @property
    def outdoor_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_OUTDOOR_TEMPERATURE))

    @property
    def program(self) -> str:
        return self.extract_property_value(PROPERTY_PROGRAM)

    @property
    def possible_programs(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_PROGRAM)

    @property
    def supports_program(self) -> bool:
        return self.has_property(PROPERTY_PROGRAM)

    @property
    def operation_mode(self) -> str:
        return self.extract_property_value(PROPERTY_OPERATION_MODE)

    @property
    def possible_operation_modes(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_OPERATION_MODE)

    @property
    def fan_speed(self) -> str:
        return self.extract_property_value(PROPERTY_FAN_SPEED)

    @property
    def possible_fan_speeds(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_FAN_SPEED)

    @property
    def supports_fan_speed(self) -> bool:
        return self.has_property(PROPERTY_FAN_SPEED)

    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def is_status_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_ON

    @property
    def overrule_active(self) -> str:
        return self.extract_property_value(PROPERTY_OVERRULE_ACTIVE)

    @property
    def is_overrule_active(self) -> bool:
        return self.overrule_active == PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE

    @property
    def supports_overrule_active(self) -> bool:
        return self.has_property(PROPERTY_OVERRULE_ACTIVE)

    @property
    def coupling_status(self) -> str:
        return self.extract_property_value(PROPERTY_COUPLING_STATUS)

    @property
    def possible_coupling_status(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_COUPLING_STATUS)

    @property
    def supports_coupling_status(self) -> bool:
        return self.has_property(PROPERTY_COUPLING_STATUS) and self.coupling_status in self.possible_coupling_status

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def set_temperature(self, gateway, temperature: float):
        gateway.add_device_control(self.uuid, PROPERTY_SETPOINT_TEMPERATURE, str(temperature))

    def set_program(self, gateway, program: str):
        gateway.add_device_control(self.uuid, PROPERTY_PROGRAM, program)

    def set_operation_mode(self, gateway, operation_mode: str):
        gateway.add_device_control(self.uuid, PROPERTY_OPERATION_MODE, operation_mode)

    def set_fan_speed(self, gateway, fan_speed: str):
        gateway.add_device_control(self.uuid, PROPERTY_FAN_SPEED, fan_speed)

    def set_status(self, gateway, status: bool):
        if status:
            gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON)
        else:
            gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF)

    def set_overrule_active(self, gateway, active: bool):
        if active:
            gateway.add_device_control(self.uuid, PROPERTY_OVERRULE_ACTIVE, PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE)
        else:
            gateway.add_device_control(self.uuid, PROPERTY_OVERRULE_ACTIVE, PROPERTY_OVERRULE_ACTIVE_VALUE_FALSE)
