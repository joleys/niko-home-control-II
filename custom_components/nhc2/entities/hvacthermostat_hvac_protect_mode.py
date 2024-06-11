from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from ..nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhc_entity import NHCBaseEntity


class Nhc2HvacthermostatHvacProtectModeEntity(NHCBaseEntity, SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoHvacthermostatHvac, hub, gateway):
        """Initialize a switch sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_protect_mode'
        self._attr_device_class = SwitchDeviceClass.SWITCH

    @property
    def name(self) -> str:
        return 'Protect Mode'

    @property
    def is_on(self) -> bool:
        return self._device.is_protect_mode

    async def async_turn_on(self, **kwargs):
        self._device.set_protect_mode(self._gateway, True)
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        self._device.set_protect_mode(self._gateway, False)
        self.schedule_update_ha_state()
