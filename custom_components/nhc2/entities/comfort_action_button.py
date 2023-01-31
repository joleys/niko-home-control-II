from homeassistant.components.button import ButtonEntity

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.comfort_action import CocoComfortAction


class Nhc2ComfortActionButtonEntity(ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoComfortAction, hub, gateway):
        """Initialize a button."""
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

    def press(self) -> None:
        """Pass - not in use."""
        pass

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_press(self):
        self._device.press(self._gateway)
        self.on_change()
