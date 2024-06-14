from ..const import PROPERTY_PROGRAM, PROPERTY_AMBIENT_TEMPERATURE, PROPERTY_SETPOINT_TEMPERATURE, \
    PROPERTY_OVERRULE_ACTIVE, PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE, PROPERTY_OVERRULE_ACTIVE_VALUE_FALSE, \
    PROPERTY_OVERRULE_SETPOINT, PROPERTY_OVERRULE_TIME, PROPERTY_ECOSAVE, PROPERTY_ECOSAVE_VALUE_TRUE, \
    PROPERTY_ECOSAVE_VALUE_FALSE, PROPERTY_PROTECT_MODE, PROPERTY_PROTECT_MODE_VALUE_TRUE, \
    PROPERTY_PROTECT_MODE_VALUE_FALSE, PROPERTY_OPERATION_MODE, PROPERTY_OPERATION_MODE_VALUE_HEATING, \
    PROPERTY_OPERATION_MODE_VALUE_COOLING, PROPERTY_FAN_SPEED, PROPERTY_FAN_SPEED_VALUE_LOW, \
    PROPERTY_FAN_SPEED_VALUE_MEDIUM, PROPERTY_FAN_SPEED_VALUE_HIGH, PROPERTY_THERMOSTAT_ON, \
    PROPERTY_THERMOSTAT_ON_VALUE_TRUE, PROPERTY_THERMOSTAT_ON_VALUE_FALSE, PROPERTY_HVAC_ON, PROPERTY_HVAC_ON_VALUE_TRUE
from ..helpers import to_float_or_none, to_int_or_none
from .device import CoCoDevice


class CocoHvacthermostatHvac(CoCoDevice):
    @property
    def program(self) -> str:
        return self.extract_property_value(PROPERTY_PROGRAM)

    @property
    def possible_programs(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_PROGRAM)

    @property
    def ambient_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_AMBIENT_TEMPERATURE))

    @property
    def ambient_temperature_range(self) -> list:
        return self.extract_property_definition_description_range(PROPERTY_AMBIENT_TEMPERATURE)

    @property
    def setpoint_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_SETPOINT_TEMPERATURE))

    @property
    def overrule_active(self) -> str:
        return self.extract_property_value(PROPERTY_OVERRULE_ACTIVE)

    @property
    def is_overrule_active(self) -> bool:
        return self.overrule_active == PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE

    @property
    def overrule_setpoint(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_OVERRULE_SETPOINT))

    @property
    def overrule_time(self) -> int:
        return to_int_or_none(self.extract_property_value(PROPERTY_OVERRULE_TIME))

    @property
    def ecosave(self) -> str:
        return self.extract_property_value(PROPERTY_ECOSAVE)

    @property
    def is_ecosave(self) -> bool:
        return self.ecosave == PROPERTY_ECOSAVE_VALUE_TRUE

    @property
    def protect_mode(self) -> str:
        return self.extract_property_value(PROPERTY_PROTECT_MODE)

    @property
    def is_protect_mode(self) -> bool:
        return self.protect_mode == PROPERTY_PROTECT_MODE_VALUE_TRUE

    @property
    def operation_mode(self) -> str:
        return self.extract_property_value(PROPERTY_OPERATION_MODE)

    @property
    def is_operation_mode_heating(self) -> bool:
        return self.operation_mode == PROPERTY_OPERATION_MODE_VALUE_HEATING

    @property
    def is_operation_mode_cooling(self) -> bool:
        return self.operation_mode == PROPERTY_OPERATION_MODE_VALUE_COOLING

    @property
    def fan_speed(self) -> str:
        return self.extract_property_value(PROPERTY_FAN_SPEED)

    @property
    def is_fan_speed_low(self) -> bool:
        return self.fan_speed == PROPERTY_FAN_SPEED_VALUE_LOW

    @property
    def is_fan_speed_medium(self) -> bool:
        return self.fan_speed == PROPERTY_FAN_SPEED_VALUE_MEDIUM

    @property
    def is_fan_speed_high(self) -> bool:
        return self.fan_speed == PROPERTY_FAN_SPEED_VALUE_HIGH

    @property
    def thermostat_on(self) -> str:
        return self.extract_property_value(PROPERTY_THERMOSTAT_ON)

    @property
    def is_thermostat_on(self) -> bool:
        return self.thermostat_on == PROPERTY_THERMOSTAT_ON_VALUE_TRUE

    @property
    def hvac_on(self) -> str:
        return self.extract_property_value(PROPERTY_HVAC_ON)

    @property
    def is_hvac_on(self) -> bool:
        return self.hvac_on == PROPERTY_HVAC_ON_VALUE_TRUE

    def set_program(self, gateway, program: str):
        gateway.add_device_control(self.uuid, PROPERTY_PROGRAM, program)

    def set_temperature(self, gateway, temperature: float):
        gateway.add_device_control(self.uuid, PROPERTY_OVERRULE_SETPOINT, str(temperature))
        gateway.add_device_control(self.uuid, PROPERTY_OVERRULE_TIME, '240')
        gateway.add_device_control(self.uuid, PROPERTY_OVERRULE_ACTIVE, 'True')

    def set_operation_mode(self, gateway, operation_mode: str):
        gateway.add_device_control(self.uuid, PROPERTY_OPERATION_MODE, operation_mode)

    def set_fan_speed(self, gateway, fan_speed: str):
        gateway.add_device_control(self.uuid, PROPERTY_FAN_SPEED, fan_speed)

    def set_overrule_active(self, gateway, active: bool):
        if active:
            gateway.add_device_control(
                self.uuid,
                PROPERTY_OVERRULE_ACTIVE,
                PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE
            )
        else:
            gateway.add_device_control(
                self.uuid,
                PROPERTY_OVERRULE_ACTIVE,
                PROPERTY_OVERRULE_ACTIVE_VALUE_FALSE
            )

    def set_ecosave(self, gateway, active: bool):
        if active:
            gateway.add_device_control(
                self.uuid,
                PROPERTY_ECOSAVE,
                PROPERTY_ECOSAVE_VALUE_TRUE
            )
        else:
            gateway.add_device_control(
                self.uuid,
                PROPERTY_ECOSAVE,
                PROPERTY_ECOSAVE_VALUE_FALSE
            )

    def set_protect_mode(self, gateway, active: bool):
        if active:
            gateway.add_device_control(
                self.uuid,
                PROPERTY_PROTECT_MODE,
                PROPERTY_PROTECT_MODE_VALUE_TRUE
            )
        else:
            gateway.add_device_control(
                self.uuid,
                PROPERTY_PROTECT_MODE,
                PROPERTY_PROTECT_MODE_VALUE_FALSE
            )

    def set_thermostat_on(self, gateway, active: bool):
        if active:
            gateway.add_device_control(
                self.uuid,
                PROPERTY_THERMOSTAT_ON,
                PROPERTY_THERMOSTAT_ON_VALUE_TRUE
            )
        else:
            gateway.add_device_control(
                self.uuid,
                PROPERTY_THERMOSTAT_ON,
                PROPERTY_THERMOSTAT_ON_VALUE_FALSE
            )
