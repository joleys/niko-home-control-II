from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS
from homeassistant.exceptions import HomeAssistantError

from ..const import DOMAIN, BRAND, LIGHT

from ..nhccoco.devices.light_action import CocoLightAction

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2LightEntity(LightEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoLightAction, hub, gateway):
        """Initialize a light."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device._after_change_callback = self.on_change

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        if self._device.support_brightness:
            self._attr_supported_color_modes = {ColorMode.BRIGHTNESS, ColorMode.ONOFF}
            self._attr_color_mode = ColorMode.BRIGHTNESS
        else:
            self._attr_supported_color_modes = {ColorMode.ONOFF}
            self._attr_color_mode = ColorMode.ONOFF

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': BRAND,
            'model': LIGHT,
            'via_device': self._hub
        }

    @property
    def is_on(self) -> bool:
        return self._device.is_on

    @property
    def brightness(self) -> int:
        if not self._device.support_brightness:
            return None

        if not self.is_on:
            return 0

        return int(round(255 * self._device.status_brightness / 100))

    def turn_off(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def turn_on(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_turn_on(self, **kwargs):
        brightness = kwargs.get(ATTR_BRIGHTNESS)

        if self._device.support_brightness and brightness is not None:
            brightness_percentage = int(round(brightness / 255 * 100))

            if brightness_percentage == 0:
                await self._device.async_turn_off()
                return

            self._gateway._add_device_control(self._device.uuid, "Brightness", str(brightness_percentage))

        self._gateway._add_device_control(self._device.uuid, "Status", "On")
        self.on_change()

    async def async_turn_off(self, **kwargs):
        self._gateway._add_device_control(self._device.uuid, "Status", "Off")
        self.on_change()

    async def _service_set_light_brightness(self, light_brightness: int) -> bool:
        if not self._device.support_brightness:
            raise HomeAssistantError(f'{self.name} does not support brightness.')
            return False

        self._gateway._add_device_control(self._device.uuid, "Brightness", str(light_brightness))
        return True
