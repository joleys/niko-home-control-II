from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS
from homeassistant.exceptions import HomeAssistantError

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.relay_action import CocoRelayAction


class Nhc2RelayActionLightEntity(LightEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoRelayAction, hub, gateway):
        """Initialize a light."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

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
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def is_on(self) -> bool:
        return self._device.is_status_on

    @property
    def brightness(self) -> int:
        if not self._device.support_brightness:
            return None

        return int(round(255 * self._device.brightness / 100))

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_turn_on(self, **kwargs):
        brightness = kwargs.get(ATTR_BRIGHTNESS)

        if self._device.support_brightness and brightness is not None:
            brightness_percentage = int(round(brightness / 255 * 100))

            if brightness_percentage == 0:
                await self._device.turn_off(self._gateway)
                return

            self._device.set_brightness(self._gateway, brightness_percentage)

        self._device.turn_on(self._gateway)
        self.on_change()

    async def async_turn_off(self):
        self._device.turn_off(self._gateway)
        self.on_change()

    async def _service_set_light_brightness(self, light_brightness: int) -> bool:
        if not self._device.support_brightness:
            raise HomeAssistantError(f'{self.name} does not support brightness.')
            return False

        self._device.set_brightness(self._gateway, light_brightness)
        return True
