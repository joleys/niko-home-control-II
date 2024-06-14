from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.util.percentage import ordered_list_item_to_percentage, percentage_to_ordered_list_item

from ..nhccoco.devices.generic_fan import CocoGenericFan
from .nhc_entity import NHCBaseEntity

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2GenericFanFanEntity(NHCBaseEntity, FanEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoGenericFan, hub, gateway):
        """Initialize a fan."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid
        self._attr_supported_features = FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE

    @property
    def is_on(self) -> bool:
        return self._device.is_status_on

    @property
    def preset_mode(self) -> str:
        if self._device.supports_program:
            return self._device.program

        if not self._device.is_fan_speed_range:
            return self._device.fan_speed

        return None

    @property
    def preset_modes(self) -> str:
        if self._device.supports_program:
            return self._device.possible_programs

        if not self._device.is_fan_speed_range:
            return self._device.possible_fan_speeds

        return None

    @property
    def percentage(self) -> int:
        if not self._device.is_fan_speed_range:
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

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if self._device.supports_program:
            self._device.set_program(self._gateway, preset_mode)
        if not self._device.is_fan_speed_range:
            self._device.set_fan_speed(self._gateway, preset_mode)

        self.schedule_update_ha_state()

    async def async_set_percentage(self, percentage: int) -> None:
        if self._device.is_fan_speed_range:
            self._device.set_fan_speed(self._gateway, percentage)
        else:
            self._device.set_fan_speed(self._gateway, percentage_to_ordered_list_item(self.preset_modes, percentage))
        self.schedule_update_ha_state()

    async def async_turn_on(self, speed: str = None, percentage: int = None, preset_mode: str = None, **kwargs) -> None:
        if not self._device.supports_status:
            _LOGGER.info('Device does not support the status property, therefor we can not set any status.')
        else:
            self._device.set_status(self._gateway, True)

        if percentage is not None and self._device.is_fan_speed_range:
            self._device.set_fan_speed(self._gateway, percentage)
        if preset_mode is not None and self._device.supports_program:
            self._device.set_program(self._gateway, preset_mode)
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        if not self._device.supports_status:
            _LOGGER.info('Device does not support the status property, therefor we can not set any status.')
            return
        self._device.set_status(self._gateway, False)
        self.schedule_update_ha_state()
