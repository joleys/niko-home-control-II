from homeassistant.components.climate import ClimateEntity, HVACMode, HVACAction, ClimateEntityFeature, \
    ATTR_TEMPERATURE, FAN_LOW, FAN_MEDIUM, FAN_HIGH, PRESET_COMFORT, PRESET_ECO, PRESET_SLEEP

from homeassistant.const import UnitOfTemperature

from ..const import DOMAIN, BRAND

from ..nhccoco.const import PROPERTY_OPERATION_MODE_VALUE_HEATING, PROPERTY_OPERATION_MODE_VALUE_COOLING, \
    PROPERTY_FAN_SPEED_VALUE_LOW, PROPERTY_FAN_SPEED_VALUE_MEDIUM, PROPERTY_FAN_SPEED_VALUE_HIGH, \
    PROPERTY_PROGRAM_VALUE_DAY, PROPERTY_PROGRAM_VALUE_ECO, PROPERTY_PROGRAM_VALUE_NIGHT

from ..nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac


class Nhc2HvacthermostatHvacClimateEntity(ClimateEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoHvacthermostatHvac, hub, gateway):
        """Initialize a climate entity."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        min_value, max_value, step = self._device.ambient_temperature_range
        self._attr_target_temperature_step = step
        self._attr_max_temp = max_value
        self._attr_min_temp = min_value
        self._attr_hvac_modes = [
            HVACMode.HEAT,
            HVACMode.COOL,
        ]
        self._attr_fan_modes = [
            FAN_LOW,
            FAN_MEDIUM,
            FAN_HIGH,
        ]
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE \
                                        | ClimateEntityFeature.FAN_MODE

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
    def hvac_action(self):
        if self._device.is_operation_mode_heating:
            return HVACAction.HEATING
        if self._device.is_operation_mode_cooling:
            return HVACAction.COOLING

        return HVACAction.IDLE

    @property
    def hvac_mode(self):
        if self._device.is_operation_mode_heating:
            return HVACMode.HEAT
        if self._device.is_operation_mode_cooling:
            return HVACMode.COOL

    @property
    def preset_mode(self) -> str:
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

    @property
    def fan_mode(self) -> str | None:
        if self._device.fan_speed == PROPERTY_FAN_SPEED_VALUE_LOW:
            return FAN_LOW
        if self._device.fan_speed == PROPERTY_FAN_SPEED_VALUE_MEDIUM:
            return FAN_MEDIUM
        if self._device.fan_speed == PROPERTY_FAN_SPEED_VALUE_HIGH:
            return FAN_HIGH

        return self._device.fan_speed

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: str):
        if hvac_mode == HVACMode.HEAT:
            self._device.set_operation_mode(self._gateway, PROPERTY_OPERATION_MODE_VALUE_HEATING)
        if hvac_mode == HVACMode.COOL:
            self._device.set_operation_mode(self._gateway, PROPERTY_OPERATION_MODE_VALUE_COOLING)
        self.on_change()

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

    def async_set_fan_mode(self, fan_mode: str):
        if fan_mode == FAN_LOW:
            self._device.set_fan_speed(self._gateway, PROPERTY_FAN_SPEED_VALUE_LOW)
        if fan_mode == FAN_MEDIUM:
            self._device.set_fan_speed(self._gateway, PROPERTY_FAN_SPEED_VALUE_MEDIUM)
        if fan_mode == FAN_HIGH:
            self._device.set_fan_speed(self._gateway, PROPERTY_FAN_SPEED_VALUE_HIGH)
        self.on_change()

    async def async_set_temperature(self, **kwargs):
        temperature = float(kwargs.get(ATTR_TEMPERATURE))
        self._device.set_temperature(self._gateway, temperature)
        self.on_change()
