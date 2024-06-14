from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from ..nhccoco.devices.relay_action import CocoRelayAction
from .nhc_entity import NHCBaseEntity


class Nhc2RelayActionSwitchEntity(NHCBaseEntity, SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoRelayAction, hub, gateway):
        """Initialize a switch."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid

    @property
    def device_class(self) -> str:
        if self._device.model == 'socket':
            return SwitchDeviceClass.OUTLET

        return SwitchDeviceClass.SWITCH

    @property
    def is_on(self) -> bool:
        return self._device.is_status_on

    async def async_turn_on(self):
        self._device.turn_on(self._gateway)
        self.schedule_update_ha_state()

    async def async_turn_off(self):
        self._device.turn_off(self._gateway)
        self.schedule_update_ha_state()
