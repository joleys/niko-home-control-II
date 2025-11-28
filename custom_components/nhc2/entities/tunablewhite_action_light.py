from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS, ATTR_HS_COLOR, \
    ATTR_COLOR_TEMP_KELVIN
from homeassistant.exceptions import HomeAssistantError

from ..nhccoco.devices.tunablewhite_action import CocoTunablewhiteAction
from .nhc_entity import NHCBaseEntity

import colorsys


class Nhc2TunablewhiteActionLightEntity(NHCBaseEntity, LightEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoTunablewhiteAction, hub, gateway):
        """Initialize a light."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid

        if self._device.support_tunable_white and self._device.support_brightness:
            self._attr_supported_color_modes = {ColorMode.COLOR_TEMP}
            self._attr_color_mode = ColorMode.COLOR_TEMP
        elif self._device.support_brightness:
            self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
            self._attr_color_mode = ColorMode.BRIGHTNESS
        else:
            self._attr_supported_color_modes = {ColorMode.ONOFF}
            self._attr_color_mode = ColorMode.ONOFF

    @property
    def is_on(self) -> bool:
        return self._device.is_status_on

    async def async_turn_on(self, **kwargs):
        brightness = kwargs.get(ATTR_BRIGHTNESS)
        color_temp_kelvin = kwargs.get(ATTR_COLOR_TEMP_KELVIN)

        if self._device.support_tunable_white and color_temp_kelvin is not None:
            self._device.set_tunable_white(self._gateway, color_temp_kelvin)

        if self._device.support_brightness and brightness is not None:
            brightness_percentage = int(round(brightness / 255 * 100))

            if brightness_percentage == 0:
                await self._device.turn_off(self._gateway)
                return

            self._device.set_brightness(self._gateway, brightness_percentage)

        self._device.turn_on(self._gateway)
        self.schedule_update_ha_state()

    async def async_turn_off(self):
        self._device.turn_off(self._gateway)
        self.schedule_update_ha_state()

    @property
    def brightness(self) -> int:
        if not self._device.support_brightness:
            return None

        return int(round(255 * self._device.brightness / 100))

    async def _service_set_light_brightness(self, light_brightness: int) -> bool:
        if not self._device.support_brightness:
            raise HomeAssistantError(f'{self.name} does not support brightness.')

        self._device.set_brightness(self._gateway, light_brightness)
        return True

    @property
    def color_temp_kelvin(self) -> int | None:
        if not self._device.support_tunable_white:
            return None

        tunable_white = self._device.tunable_white
        if tunable_white is None:
            return None

        color_temp, _brightness = tunable_white
        return int(round(color_temp))

    @property
    def max_color_temp_kelvin(self) -> int | None:
        if not self._device.support_tunable_white:
            return None

        return 6500

    @property
    def min_color_temp_kelvin(self) -> int | None:
        if not self._device.support_tunable_white:
            return None

        return 2700
