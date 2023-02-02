from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.flag_action import CocoFlagAction


class Nhc2FlagActionSwitchEntity(SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoFlagAction, hub, gateway):
        """Initialize a switch."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

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

    def turn_off(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def turn_on(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_turn_on(self):
        self._device.turn_on(self._gateway)
        self.on_change()

    async def async_turn_off(self):
        self._device.turn_off(self._gateway)
        self.on_change()
