from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from ..nhccoco.devices.relay_action import CocoRelayAction


class Nhc2RelayActionSwitchEntity(SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoRelayAction, hub, gateway):
        """Initialize a switch."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

    @property
    def device_class(self) -> str:
        if self._device.model == 'socket':
            return SwitchDeviceClass.OUTLET

        return SwitchDeviceClass.SWITCH

    @property
    def is_on(self) -> bool:
        return self._device.is_status_on

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_turn_on(self):
        self._device.turn_on(self._gateway)
        self.on_change()

    async def async_turn_off(self):
        self._device.turn_off(self._gateway)
        self.on_change()
