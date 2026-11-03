from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.util.percentage import ordered_list_item_to_percentage, percentage_to_ordered_list_item

from ..nhccoco.devices.flux_fan import CocoFluxFan
from .nhc_entity import NHCBaseEntity


class Nhc2FluxFanFanEntity(NHCBaseEntity, FanEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoFluxFan, hub, gateway):
        """Initialize a fan."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid

        self._attr_supported_features = FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE

    @property
    def is_on(self) -> bool:
        return True

    @property
    def preset_mode(self) -> str:
        return self._device.fan_speed

    @property
    def preset_modes(self) -> list:
        return self._device.possible_fan_speeds

    @property
    def percentage(self) -> int:
        return ordered_list_item_to_percentage(self._device.possible_fan_speeds, self._device.fan_speed)

    @property
    def speed_count(self) -> int:
        return len(self._device.possible_fan_speeds)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        self._device.set_fan_speed(self._gateway, preset_mode)
        self.schedule_update_ha_state()

    async def async_set_percentage(self, percentage: int) -> None:
        self._device.set_fan_speed(self._gateway, percentage_to_ordered_list_item(self.preset_modes, percentage))
        self.schedule_update_ha_state()
