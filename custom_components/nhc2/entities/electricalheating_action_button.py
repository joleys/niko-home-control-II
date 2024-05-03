from homeassistant.components.button import ButtonEntity

from ..nhccoco.devices.electricalheating_action import CocoElectricalheatingAction


class Nhc2ElectricalHeatingActionButtonEntity(ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoElectricalheatingAction, hub, gateway):
        """Initialize a button."""
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

    async def async_press(self) -> None:
        self._device.press(self._gateway)
        self.on_change()
