from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.util.percentage import ordered_list_item_to_percentage, percentage_to_ordered_list_item

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.fan_action import CocoFanAction


class Nhc2FanActionFanEntity(FanEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoFanAction, hub, gateway):
        """Initialize a switch."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        self._attr_supported_features = FanEntityFeature.SET_SPEED, FanEntityFeature.PRESET_MODE

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
        return self._device.fan_speed

    @property
    def preset_modes(self) -> str:
        return self._device.possible_fan_speeds

    @property
    def percentage(self) -> int:
        """Return the current speed percentage."""
        return ordered_list_item_to_percentage(self.preset_modes, self._device.fan_speed)

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return len(self.preset_modes)

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        self._device.set_fan_speed(self._gateway, preset_mode)
        self.on_change()

    async def async_set_percentage(self, percentage: int) -> None:
        self._device.set_fan_speed(self._gateway, percentage_to_ordered_list_item(self.preset_modes, percentage))
        self.on_change()
