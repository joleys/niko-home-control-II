from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from ..nhccoco.devices.generic_fan import CocoGenericFan
from .nhc_entity import NHCBaseEntity


class Nhc2GenericFanBoostEntity(NHCBaseEntity, SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericFan, hub, gateway):
        """Initialize a switch sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_boost'
        self._attr_device_class = SwitchDeviceClass.SWITCH

    @property
    def name(self) -> str:
        return 'Boost'

    @property
    def is_on(self) -> bool:
        return self._device.is_boost

    async def async_turn_on(self, **kwargs):
        self._device.set_boost(self._gateway, True)
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        self._device.set_boost(self._gateway, False)
        self.schedule_update_ha_state()
