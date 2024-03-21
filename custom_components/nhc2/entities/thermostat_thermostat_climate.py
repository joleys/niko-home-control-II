from homeassistant.components.climate import ClimateEntity, HVACMode, HVACAction, ClimateEntityFeature, \
    ATTR_TEMPERATURE, PRESET_COMFORT, PRESET_ECO, PRESET_SLEEP
from homeassistant.const import UnitOfTemperature

from ..const import DOMAIN, BRAND
from ..nhccoco.const import PROPERTY_PROGRAM_VALUE_DAY, PROPERTY_PROGRAM_VALUE_ECO, PROPERTY_PROGRAM_VALUE_NIGHT, \
    PROPERTY_PROGRAM_VALUE_OFF, PROPERTY_PROGRAM_VALUE_PROG_1

from ..nhccoco.devices.thermostat_thermostat import CocoThermostatThermostat


class Nhc2ThermostatThermostatClimateEntity(ClimateEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoThermostatThermostat, hub, gateway):
        """Initialize a climate entity."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        min_value, max_value, step = self._device.overrule_setpoint_range

        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_precision = step
        self._attr_target_temperature_high = max_value
        self._attr_target_temperature_low = min_value
        self._attr_target_temperature_step = step
        self._attr_max_temp = max_value
        self._attr_min_temp = min_value
        self._enable_turn_on_off_backwards_compatibility = False
        self._attr_supported_features = (ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
                                         | ClimateEntityFeature.TURN_OFF)
        self._attr_hvac_modes = [
            HVACMode.AUTO,
            HVACMode.HEAT_COOL,
            HVACMode.OFF,
        ]

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': BRAND,
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def current_temperature(self) -> float:
        return self._device.ambient_temperature

    @property
    def target_temperature(self) -> float:
        return self._device.setpoint_temperature

    @property
    def hvac_mode(self):
        if self._device.is_demand_heating:
            return HVACMode.HEAT
        if self._device.is_demand_cooling:
            return HVACMode.COOL
        if self._device.is_demand_none:
            return HVACMode.OFF

    @property
    def hvac_action(self):
        if self._device.program == PROPERTY_PROGRAM_VALUE_OFF:
            return HVACAction.OFF
        if self._device.is_demand_heating:
            return HVACAction.HEATING
        if self._device.is_demand_cooling:
            return HVACAction.COOLING

        return HVACAction.IDLE

    @property
    def preset_mode(self) -> str:
        if self._device.program == PROPERTY_PROGRAM_VALUE_ECO:
            return PRESET_ECO
        if self._device.program == PROPERTY_PROGRAM_VALUE_DAY:
            return PRESET_COMFORT
        if self._device.program == PROPERTY_PROGRAM_VALUE_NIGHT:
            return PRESET_SLEEP

        return self._device.program

    @property
    def preset_modes(self) -> list[str]:
        modes = []
        for program in self._device.possible_programs:
            if program == PROPERTY_PROGRAM_VALUE_ECO:
                modes.append(PRESET_ECO)
            elif program == PROPERTY_PROGRAM_VALUE_DAY:
                modes.append(PRESET_COMFORT)
            elif program == PROPERTY_PROGRAM_VALUE_NIGHT:
                modes.append(PRESET_SLEEP)
            else:
                modes.append(program)

        return modes

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: str):
        if hvac_mode == HVACMode.AUTO or hvac_mode == HVACMode.HEAT_COOL:
            self._device.set_program(self._gateway, PROPERTY_PROGRAM_VALUE_PROG_1)
        if hvac_mode == HVACMode.OFF:
            self._device.set_program(self._gateway, PROPERTY_PROGRAM_VALUE_OFF)

        self.on_change()

    async def async_set_preset_mode(self, preset_mode: str):
        if preset_mode == PRESET_ECO:
            program = PROPERTY_PROGRAM_VALUE_ECO
        elif preset_mode == PRESET_COMFORT:
            program = PROPERTY_PROGRAM_VALUE_DAY
        elif preset_mode == PRESET_SLEEP:
            program = PROPERTY_PROGRAM_VALUE_NIGHT
        else:
            program = preset_mode

        self._device.set_program(self._gateway, program)
        self.on_change()

    async def async_set_temperature(self, **kwargs):
        temperature = float(kwargs.get(ATTR_TEMPERATURE))
        self._device.set_temperature(self._gateway, temperature)
        self.on_change()

    async def async_turn_off(self):
        self._device.set_program(self._gateway, PROPERTY_PROGRAM_VALUE_OFF)
        self.on_change()