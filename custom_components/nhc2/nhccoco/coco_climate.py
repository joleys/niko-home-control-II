import logging

from .helpers import status_prop_in_object_is_on, extract_property_definitions, extract_property_value_from_device
from .const import THERM_PROGRAM, THERM_OVERRULEACTION, THERM_OVERRULESETPOINT, THERM_OVERRULETIME, THERM_ECOSAVE
from .coco_entity import CoCoEntity

from homeassistant.components.climate import (
    TEMP_CELSIUS,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_TEMPERATURE_RANGE,
    SUPPORT_PRESET_MODE, 
    HVAC_MODE_HEAT,
    HVAC_MODE_HEAT_COOL
)

_LOGGER = logging.getLogger(__name__)

class CoCoThermostat(CoCoEntity):

    @property
    def state(self):
        return self._state

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def target_temperature_low(self):
        return self._target_temperature_low

    @property
    def target_temperature_high(self):
        return self._target_temperature_high

    @property
    def target_temperature_step(self):
        return self._target_temperature_step

    @property
    def min_temp(self):
        return self._min_temp

    @property
    def max_temp(self):
        return self._max_temp

    @property
    def hvac_action(self):
        """Return current operation ie. heating, cooling, off."""
        return self._hvac_action

    @property
    def hvac_mode(self):
        """Return current operation ie. heating, cooling, off."""
        return self._hvac_mode

    @property
    def hvac_modes(self):
        return HVAC_MODE_HEAT_COOL

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def program(self):
        return self._program

    @property
    def preset_mode(self):
        return self._preset_mode

    @property
    def preset_modes(self):
        return self._preset_modes

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._current_temperature = None
        self._target_temperature = None
        self._preset_mode = None
        self._hvac_mode = None
        self._program = None
        self.update_dev(dev, callback_container)

        self.get_target_temperature_params(dev)
        self.get_ambient_temperature_params(dev)
        self.get_program_params(dev)

    async def async_turn_on(self):
        pass

    async def async_turn_off(self):
        pass

    def set_temperature(self, temperature):
        _LOGGER.info('Set temperature: %s', temperature)
        self._command_device_control(self._uuid, THERM_OVERRULESETPOINT, str(temperature))
        self._command_device_control(self._uuid, THERM_OVERRULETIME, str(480))
        self._command_device_control(self._uuid, THERM_OVERRULEACTION, 'True')

    def set_preset_mode(self, preset_mode):
        """Set preset mode."""
        _LOGGER.info('Set preset mode: %s', preset_mode)
        self._command_device_control(self._uuid, THERM_PROGRAM, preset_mode)

    def get_target_temperature_params(self, dev):
        """Get parameters for target temperature"""
        if dev and 'PropertyDefinitions' in dev:
            params = extract_property_definitions(dev, 'SetpointTemperature')['Description']
            values = params.split("(")[1].split(")")[0].split(",")
            self._target_temperature_low = float(values[0])
            self._target_temperature_high = float(values[1])
            self._target_temperature_step = float(values[2])

    def get_ambient_temperature_params(self, dev):
        """Get parameters for ambient temperature"""
        if dev and 'PropertyDefinitions' in dev:
            params = extract_property_definitions(dev, 'AmbientTemperature')['Description']
            values = params.split("(")[1].split(")")[0].split(",")
            self._min_temp = float(values[0])
            self._max_temp = float(values[1])

    def get_program_params(self, dev):
        """Get parameters for programs"""
        if dev and 'PropertyDefinitions' in dev:
            params = extract_property_definitions(dev, 'Program')['Description']
            values = params.split("(")[1].split(")")[0].split(",")
            self._preset_modes = values

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        if self._check_for_status_change(dev):
            self._current_temperature = float(extract_property_value_from_device(dev, 'AmbientTemperature'))
            self._target_temperature = float(extract_property_value_from_device(dev, 'SetpointTemperature'))
            self._preset_mode = extract_property_value_from_device(dev, 'Program')
            self._hvac_mode = extract_property_value_from_device(dev, 'Demand')
            self._hvac_action = extract_property_value_from_device(dev, 'Demand')
            has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()

    def _check_for_status_change(self, dev):
        status_value = extract_property_value_from_device(dev, 'AmbientTemperature')
        if status_value and self._current_temperature != status_value:
            self._current_temperature = float(status_value)
            has_changed = True
        status_value = extract_property_value_from_device(dev, 'SetpointTemperature')
        if status_value and self._target_temperature != status_value:
            self._target_temperature = float(status_value)
            has_changed = True
        status_value = extract_property_value_from_device(dev, 'Program')
        if status_value and self._preset_mode != status_value:
            self._preset_mode = status_value
            has_changed = True
        status_value = extract_property_value_from_device(dev, 'Demand')
        if status_value and self._hvac_mode != status_value:
            self._hvac_mode = status_value
            has_changed = True
        return has_changed
