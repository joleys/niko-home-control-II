from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.util.percentage import ordered_list_item_to_percentage, percentage_to_ordered_list_item

from ..nhccoco.devices.fan_action import CocoFanAction
from .nhc_entity import NHCBaseEntity


class Nhc2FanActionFanEntity(NHCBaseEntity, FanEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoFanAction, hub, gateway):
        """Initialize a fan."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid

        self._attr_supported_features = FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE
        self._preset_modes = self._device.possible_fan_speeds

    @property
    def preset_mode(self) -> str:
        return self._device.fan_speed

    @property
    def preset_modes(self) -> str:
        return self._preset_modes

    @property
    def percentage(self) -> int:
        """Return the current speed percentage based on the current mode."""
        return ordered_list_item_to_percentage(self._preset_modes, self._device.fan_speed)

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return len(self._preset_modes)

    @property
    def supported_features(self):
        """Return supported features."""
        return self._attr_supported_features

    def set_percentage(self, percentage: int) -> None:
        """Set the fan speed preset based on a given percentage"""
        self._device.set_fan_speed(self._gateway, percentage_to_ordered_list_item(self._preset_modes, percentage))

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        self._device.set_fan_speed(self._gateway, preset_mode)
        self.schedule_update_ha_state()

    async def async_set_percentage(self, percentage: int) -> None:
        self._device.set_fan_speed(self._gateway, percentage_to_ordered_list_item(self._preset_modes, percentage))
        self.schedule_update_ha_state()
