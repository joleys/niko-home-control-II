from homeassistant.components.switch import SwitchEntity

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.relay_action import CocoRelayAction

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2SwitchEntity(SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoRelayAction, hub, gateway):
        """Initialize a light."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device._after_change_callback = self.on_change

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
            'model': f'{self._device.model} ({self._device.type})',
            'via_device': self._hub
        }

    @property
    def is_on(self) -> bool:
        return self._device.is_on

    def turn_off(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def turn_on(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_turn_on(self, **kwargs):
        self._gateway._add_device_control(self._device.uuid, "Status", "On")
        self.on_change()

    async def async_turn_off(self, **kwargs):
        self._gateway._add_device_control(self._device.uuid, "Status", "Off")
        self.on_change()
