from homeassistant.components.climate import ClimateEntity, HVACMode, HVACAction, ClimateEntityFeature, \
    ATTR_TEMPERATURE, FAN_OFF, FAN_LOW, FAN_MEDIUM, FAN_HIGH, FAN_AUTO, PRESET_COMFORT, PRESET_AWAY, PRESET_ECO, \
    PRESET_HOME, PRESET_SLEEP
from homeassistant.const import UnitOfTemperature

from ..const import DOMAIN, BRAND
from ..nhccoco.const import PROPERTY_PROGRAM_VALUE_DAY, PROPERTY_PROGRAM_VALUE_ECO, PROPERTY_PROGRAM_VALUE_NIGHT, \
    PROPERTY_PROGRAM_VALUE_AWAY, PROPERTY_PROGRAM_VALUE_HOME, PROPERTY_STATUS_VALUE_OFF, \
    PROPERTY_OPERATION_MODE_VALUE_HEAT, PROPERTY_OPERATION_MODE_VALUE_COOL, PROPERTY_OPERATION_MODE_VALUE_AUTO, \
    PROPERTY_FAN_SPEED_VALUE_OFF, PROPERTY_FAN_SPEED_VALUE_LOW, PROPERTY_FAN_SPEED_VALUE_MEDIUM, \
    PROPERTY_FAN_SPEED_VALUE_HIGH, PROPERTY_FAN_SPEED_VALUE_AUTO
from ..nhccoco.devices.generic_hvac import CocoGenericHvac


class Nhc2GenericHvacClimateEntity(ClimateEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoGenericHvac, hub, gateway):
        """Initialize a lock sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_current_temperature = self._device.ambient_temperature
        self._attr_target_temperature = self._device.setpoint_temperature
        self._attr_hvac_modes = [
            HVACMode.AUTO,
            HVACMode.HEAT_COOL,
            HVACMode.OFF,
        ]
        self._attr_fan_modes = [
            FAN_OFF,
            FAN_LOW,
            FAN_MEDIUM,
            FAN_HIGH,
            FAN_AUTO,
        ]
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE | \
                                        ClimateEntityFeature.PRESET_MODE

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': f'{BRAND} ({self._device.technology})',
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def hvac_action(self):
        if self._device.status == PROPERTY_STATUS_VALUE_OFF:
            return HVACAction.OFF
        if self._device.operation_mode == PROPERTY_OPERATION_MODE_VALUE_HEAT:
            return HVACAction.HEATING
        if self._device.operation_mode == PROPERTY_OPERATION_MODE_VALUE_COOL:
            return HVACAction.COOLING

        return HVACAction.IDLE

    @property
    def hvac_mode(self):
        if self._device.status == PROPERTY_STATUS_VALUE_OFF:
            return HVACMode.OFF

        if self._device.operation_mode == PROPERTY_OPERATION_MODE_VALUE_AUTO:
            return HVACMode.AUTO
        if self._device.operation_mode == PROPERTY_OPERATION_MODE_VALUE_HEAT:
            return HVACMode.HEAT
        if self._device.operation_mode == PROPERTY_OPERATION_MODE_VALUE_COOL:
            return HVACMode.COOL

    @property
    def preset_mode(self) -> str:
        if self._device.program == PROPERTY_PROGRAM_VALUE_ECO:
            return PRESET_ECO
        if self._device.program == PROPERTY_PROGRAM_VALUE_AWAY:
            return PRESET_AWAY
        if self._device.program == PROPERTY_PROGRAM_VALUE_DAY:
            return PRESET_COMFORT
        if self._device.program == PROPERTY_PROGRAM_VALUE_HOME:
            return PRESET_HOME
        if self._device.program == PROPERTY_PROGRAM_VALUE_NIGHT:
            return PRESET_SLEEP

        return self._device.program

    @property
    def preset_modes(self) -> list[str]:
        modes = []
        for program in self._device.possible_programs:
            if program == PROPERTY_PROGRAM_VALUE_ECO:
                modes.append(PRESET_ECO)
            elif program == PROPERTY_PROGRAM_VALUE_AWAY:
                modes.append(PRESET_AWAY)
            elif program == PROPERTY_PROGRAM_VALUE_DAY:
                modes.append(PRESET_COMFORT)
            elif program == PROPERTY_PROGRAM_VALUE_HOME:
                modes.append(PRESET_HOME)
            elif program == PROPERTY_PROGRAM_VALUE_NIGHT:
                modes.append(PRESET_SLEEP)
            else:
                modes.append(program)

        return modes

    @property
    def fan_mode(self) -> str:
        return self._device.fan_speed

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_set_temperature(self, **kwargs):
        temperature = float(kwargs.get(ATTR_TEMPERATURE))
        self._device.set_temperature(self._gateway, temperature)
        self.on_change()

    async def async_set_hvac_mode(self, hvac_mode: str):
        if hvac_mode == HVACMode.OFF:
            self._device.set_status(self._gateway, PROPERTY_STATUS_VALUE_OFF)
        if hvac_mode == HVACMode.HEAT:
            self._device.set_operation_mode(self._gateway, PROPERTY_OPERATION_MODE_VALUE_HEAT)
        if hvac_mode == HVACMode.COOL:
            self._device.set_operation_mode(self._gateway, PROPERTY_OPERATION_MODE_VALUE_COOL)
        if hvac_mode == HVACMode.AUTO or hvac_mode == HVACMode.HEAT_COOL:
            self._device.set_operation_mode((self._gateway, PROPERTY_OPERATION_MODE_VALUE_AUTO))
        self.on_change()

    async def async_set_preset_mode(self, preset_mode: str):
        if preset_mode == PRESET_ECO:
            program = PROPERTY_PROGRAM_VALUE_ECO
        elif preset_mode == PRESET_AWAY:
            program = PROPERTY_PROGRAM_VALUE_AWAY
        elif preset_mode == PRESET_COMFORT:
            program = PROPERTY_PROGRAM_VALUE_DAY
        elif preset_mode == PRESET_HOME:
            program = PROPERTY_PROGRAM_VALUE_HOME
        elif preset_mode == PRESET_SLEEP:
            program = PROPERTY_PROGRAM_VALUE_NIGHT
        else:
            program = preset_mode

        self._device.set_program(self._gateway, program)
        self.on_change()

    async def async_set_fan_mode(self, fan_mode: str):
        if fan_mode == FAN_OFF:
            fan_mode = PROPERTY_FAN_SPEED_VALUE_OFF
        elif fan_mode == FAN_LOW:
            fan_mode = PROPERTY_FAN_SPEED_VALUE_LOW
        elif fan_mode == FAN_MEDIUM:
            fan_mode = PROPERTY_FAN_SPEED_VALUE_MEDIUM
        elif fan_mode == FAN_HIGH:
            fan_mode = PROPERTY_FAN_SPEED_VALUE_HIGH
        elif fan_mode == FAN_AUTO:
            fan_mode = PROPERTY_FAN_SPEED_VALUE_AUTO
        else:
            fan_mode = fan_mode

        self._device.set_fan_speed(self._gateway, fan_mode)
        self.on_change()
