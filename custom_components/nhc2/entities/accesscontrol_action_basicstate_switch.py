from homeassistant.components.switch import SwitchEntity

from ..nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction
from .nhc_entity import NHCBaseEntity


class Nhc2AccesscontrolActionBasicStateSwitchEntity(NHCBaseEntity, SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoAccesscontrolAction, hub, gateway):
        """Initialize a switch."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_basic_switch'

    @property
    def is_on(self) -> bool:
        return self._device.is_basic_state_on

    async def async_turn_on(self):
        if not self.is_on:
            self._device.press(self._gateway)
        self.schedule_update_ha_state()

    async def async_turn_off(self):
        if self.is_on:
            self._device.press(self._gateway)
        self.schedule_update_ha_state()
