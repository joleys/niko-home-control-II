from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_PROGRAM, PROPERTY_PROGRAM_VALUE_DAY, \
    PROPERTY_PROGRAM_VALUE_ECO, PROPERTY_PROGRAM_VALUE_NIGHT, PROPERTY_PROGRAM_VALUE_OFF, PROPERTY_PROGRAM_VALUE_PROG_1, \
    PROPERTY_PROGRAM_VALUE_PROG_2, PROPERTY_PROGRAM_VALUE_PROG_3, PROPERTY_AMBIENT_TEMPERATURE, \
    PROPERTY_SETPOINT_TEMPERATURE, PROPERTY_OVERRULE_ACTIVE, PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE, \
    PROPERTY_OVERRULE_ACTIVE_VALUE_FALSE, PROPERTY_OVERRULE_SETPOINT, PROPERTY_OVERRULE_TIME, PROPERTY_ECOSAVE, \
    PROPERTY_ECOSAVE_VALUE_TRUE, PROPERTY_ECOSAVE_VALUE_FALSE, PROPERTY_DEMAND, PROPERTY_DEMAND_VALUE_HEATING, \
    PROPERTY_DEMAND_VALUE_COOLING, PROPERTY_DEMAND_VALUE_NONE
from ..helpers import to_float_or_none, to_int_or_none
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoThermostatHvac(CoCoDevice):
    @property
    def status_program(self) -> str:
        return self.extract_property_value(PROPERTY_PROGRAM)

    @property
    def possible_programs(self) -> list:
        return [
            PROPERTY_PROGRAM_VALUE_DAY,
            PROPERTY_PROGRAM_VALUE_ECO,
            PROPERTY_PROGRAM_VALUE_NIGHT,
            PROPERTY_PROGRAM_VALUE_OFF,
            PROPERTY_PROGRAM_VALUE_PROG_1,
            PROPERTY_PROGRAM_VALUE_PROG_2,
            PROPERTY_PROGRAM_VALUE_PROG_3,
        ]

    @property
    def status_ambient_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_AMBIENT_TEMPERATURE))

    @property
    def status_setpoint_temperature(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_SETPOINT_TEMPERATURE))

    @property
    def status_overrule_active(self) -> str:
        return self.extract_property_value(PROPERTY_OVERRULE_ACTIVE)

    @property
    def is_overrule_active(self) -> bool:
        return self.status_overrule_active == PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE

    @property
    def status_overrule_setpoint(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_OVERRULE_SETPOINT))

    @property
    def status_overrule_time(self) -> int:
        return to_int_or_none(self.extract_property_value(PROPERTY_OVERRULE_TIME))

    @property
    def status_ecosave(self) -> str:
        return self.extract_property_value(PROPERTY_ECOSAVE)

    @property
    def is_ecosave(self) -> bool:
        return self.status_ecosave == PROPERTY_ECOSAVE_VALUE_TRUE

    @property
    def status_demand(self) -> str:
        return self.extract_property_value(PROPERTY_DEMAND)

    @property
    def is_demand_heating(self) -> bool:
        return self.status_demand == PROPERTY_DEMAND_VALUE_HEATING

    @property
    def is_demand_cooling(self) -> bool:
        return self.status_demand == PROPERTY_DEMAND_VALUE_COOLING

    @property
    def is_demand_none(self) -> bool:
        return self.status_demand == PROPERTY_DEMAND_VALUE_NONE

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def set_program(self, gateway, program: str):
        gateway._add_device_control(
            self._device.uuid,
            PROPERTY_PROGRAM,
            program
        )

    def set_temperature(self, gateway, temperature: float):
        gateway._add_device_control(self._device.uuid, PROPERTY_OVERRULE_SETPOINT, str(temperature))
        gateway._add_device_control(self._device.uuid, PROPERTY_OVERRULE_TIME, '240')
        gateway._add_device_control(self._device.uuid, PROPERTY_OVERRULE_ACTIVE, PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE)

    def set_overrule_active(self, gateway, active: bool):
        if active:
            gateway._add_device_control(
                self._device.uuid,
                PROPERTY_OVERRULE_ACTIVE,
                PROPERTY_OVERRULE_ACTIVE_VALUE_TRUE
            )
        else:
            gateway._add_device_control(
                self._device.uuid,
                PROPERTY_OVERRULE_ACTIVE,
                PROPERTY_OVERRULE_ACTIVE_VALUE_FALSE
            )

    def set_ecosave(self, gateway, active: bool):
        if active:
            gateway._add_device_control(
                self._device.uuid,
                PROPERTY_ECOSAVE,
                PROPERTY_ECOSAVE_VALUE_TRUE
            )
        else:
            gateway._add_device_control(
                self._device.uuid,
                PROPERTY_ECOSAVE,
                PROPERTY_ECOSAVE_VALUE_FALSE
            )
