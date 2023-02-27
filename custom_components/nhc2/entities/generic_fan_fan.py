from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.util.percentage import ordered_list_item_to_percentage, percentage_to_ordered_list_item

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.generic_fan import CocoGenericFan

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2GenericFanFanEntity(FanEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoGenericFan, hub, gateway):
        """Initialize a fan."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = self._device.uuid
        self._attr_should_poll = False

        self._attr_is_on = self._device.is_status_on
        self._attr_supported_features = FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE

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
    def preset_mode(self) -> str:
        if self._device.supports_program:
            return self._device.program

        return None

    @property
    def preset_modes(self) -> str:
        if self._device.supports_program:
            return self._device.possible_programs

        return None

    @property
    def percentage(self) -> int:
        if not self._device.is_fan_speed_range:
            _LOGGER.debug(f'percentage: {self._device.is_fan_speed_range}')
            return ordered_list_item_to_percentage(self._device.possible_fan_speeds, self._device.fan_speed)

        return self._device.fan_speed

    @property
    def speed_count(self) -> int:
        if not self._device.is_fan_speed_range:
            return len(self._device.possible_fan_speeds)

        return 100

    @property
    def supported_features(self):
        """Return supported features."""
        return self._attr_supported_features

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        self._device.set_program(self._gateway, preset_mode)
        self.on_change()

    async def async_set_percentage(self, percentage: int) -> None:
        if self._device.is_fan_speed_range:
            self._device.set_fan_speed(self._gateway, percentage)
        else:
            self._device.set_fan_speed(self._gateway, percentage_to_ordered_list_item(self._preset_modes, percentage))
        self.on_change()

    async def async_turn_on(self, speed: str = None, percentage: int = None, preset_mode: str = None, **kwargs) -> None:
        self._device.set_status(self._gateway, True)
        if percentage is not None and self._device.is_fan_speed_range:
            self._device.set_fan_speed(self._gateway, percentage)
        if preset_mode is not None and self._device.supports_program:
            self._device.set_program(self._gateway, preset_mode)
        self.on_change()

    async def async_turn_off(self, **kwargs) -> None:
        self._device.set_status(self._gateway, False)
        self.on_change()
