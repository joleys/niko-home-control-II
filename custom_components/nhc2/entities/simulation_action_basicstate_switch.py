from homeassistant.components.switch import SwitchEntity

from ..nhccoco.devices.simulation_action import CocoSimulationAction


class Nhc2SimulationActionBasicStateSwitchEntity(SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoSimulationAction, hub, gateway):
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
    def is_on(self) -> bool:
        return self._device.is_basic_state_on

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_turn_on(self):
        if not self.is_on:
            self._device.press(self._gateway)
        self.on_change()

    async def async_turn_off(self):
        if self.is_on:
            self._device.press(self._gateway)
        self.on_change()
