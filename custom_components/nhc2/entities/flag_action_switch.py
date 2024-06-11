from homeassistant.components.switch import SwitchEntity

from ..nhccoco.devices.flag_action import CocoFlagAction
from .nhc_entity import NHCBaseEntity


class Nhc2FlagActionSwitchEntity(NHCBaseEntity, SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoFlagAction, hub, gateway):
        """Initialize a switch."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

    @property
    def is_on(self) -> bool:
        return self._device.is_status_on

    async def async_turn_on(self):
        self._device.turn_on(self._gateway)
        self.schedule_update_ha_state()

    async def async_turn_off(self):
        self._device.turn_off(self._gateway)
        self.schedule_update_ha_state()
