from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS
from homeassistant.exceptions import HomeAssistantError

from ..nhccoco.devices.tunablewhiteandcolor_action import CocoTunablewhiteandcolorAction
from .nhc_entity import NHCBaseEntity


class Nhc2TunablewhiteandcolorActionLightEntity(NHCBaseEntity, LightEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoTunablewhiteandcolorAction, hub, gateway):
        """Initialize a light."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid

        if self._device.support_brightness:
            self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
            self._attr_color_mode = ColorMode.BRIGHTNESS
        else:
            self._attr_supported_color_modes = {ColorMode.ONOFF}
            self._attr_color_mode = ColorMode.ONOFF

    @property
    def is_on(self) -> bool:
        return self._device.is_status_on

    @property
    def brightness(self) -> int:
        if not self._device.support_brightness:
            return None

        return int(round(255 * self._device.brightness / 100))

    async def async_turn_on(self, **kwargs):
        brightness = kwargs.get(ATTR_BRIGHTNESS)

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

    async def _service_set_light_brightness(self, light_brightness: int) -> bool:
        if not self._device.support_brightness:
            raise HomeAssistantError(f'{self.name} does not support brightness.')

        self._device.set_brightness(self._gateway, light_brightness)
        return True
