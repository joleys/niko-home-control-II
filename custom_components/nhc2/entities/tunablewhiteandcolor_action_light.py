from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS, ATTR_HS_COLOR, \
    ATTR_COLOR_TEMP_KELVIN
from homeassistant.exceptions import HomeAssistantError

from ..nhccoco.devices.tunablewhiteandcolor_action import CocoTunablewhiteandcolorAction
from .nhc_entity import NHCBaseEntity

import colorsys


class Nhc2TunablewhiteandcolorActionLightEntity(NHCBaseEntity, LightEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoTunablewhiteandcolorAction, hub, gateway):
        """Initialize a light."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid

        if self._device.support_tunable_white and self._device.support_color and self._device.support_brightness:
            self._attr_supported_color_modes = {ColorMode.HS, ColorMode.COLOR_TEMP}
        elif self._device.support_color and self._device.support_brightness:
            self._attr_supported_color_modes = {ColorMode.HS}
        elif self._device.support_brightness:
            self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        else:
            self._attr_supported_color_modes = {ColorMode.ONOFF}

    @property
    def is_on(self) -> bool:
        return self._device.is_status_on

    async def async_turn_on(self, **kwargs):
        brightness = kwargs.get(ATTR_BRIGHTNESS)
        color = kwargs.get(ATTR_HS_COLOR)
        color_temp_kelvin = kwargs.get(ATTR_COLOR_TEMP_KELVIN)

        if self._device.support_tunable_white and color_temp_kelvin is not None:
            self._device.set_tunable_white(self._gateway, color_temp_kelvin)

        if self._device.support_color and color is not None:
            brightness_percentage = int(round(self.brightness / 255 * 100))
            self._device.set_color(self._gateway, color, brightness_percentage)

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
    def hs_color(self) -> tuple[float, float] | None:
        if not self._device.support_color:
            return None

        return self._device.color

    async def _service_set_light_color(self, light_color) -> bool:
        if not self._device.support_color:
            raise HomeAssistantError(f'{self.name} does not support color.')

        # Convert RGB to HSV
        r, g, b = light_color
        r_f, g_f, b_f = r / 255.0, g / 255.0, b / 255.0
        h, s, v = colorsys.rgb_to_hsv(r_f, g_f, b_f)
        h_deg = int(round(h * 360.0))
        s_pct = int(round(s * 100.0))
        v_pct = int(round(v * 100.0))

        light_color = (h_deg, s_pct)
        light_brightness = int(round(v_pct))
        self._device.set_color(self._gateway, light_color, light_brightness)
        return True

    @property
    def color_mode(self) -> ColorMode:
        if self._device.support_tunable_white and self._device.support_color and self._device.support_brightness:
            if self._device.color_mode == "Color":
                return ColorMode.HS
            if self._device.color_mode == "TunableWhite":
                return ColorMode.COLOR_TEMP
            return ColorMode.HS
        elif self._device.support_color and self._device.support_brightness:
            return ColorMode.HS
        elif self._device.support_brightness:
            return ColorMode.BRIGHTNESS
        else:
            return ColorMode.ONOFF

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
