from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from ..nhccoco.devices.thermostat_thermostat import CocoThermostatThermostat
from .nhc_entity import NHCBaseEntity


class Nhc2ThermostatThermostatEcoSaveEntity(NHCBaseEntity, SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoThermostatThermostat, hub, gateway):
        """Initialize a switch sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_ecosave'
        self._attr_device_class = SwitchDeviceClass.SWITCH

    @property
    def name(self) -> str:
        return 'EcoSave'

    @property
    def is_on(self) -> bool:
        return self._device.is_ecosave

    async def async_turn_on(self, **kwargs):
        self._device.set_ecosave(self._gateway, True)
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        self._device.set_ecosave(self._gateway, False)
        self.schedule_update_ha_state()
