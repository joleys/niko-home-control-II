from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from ..nhccoco.devices.thermostat_hvac import CocoThermostatHvac


class Nhc2ThermostatHvacOverruleActiveEntity(SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoThermostatHvac, hub, gateway):
        """Initialize a switch sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_overrule_active'
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)
        self._attr_device_class = SwitchDeviceClass.SWITCH

    @property
    def name(self) -> str:
        return 'Overrule Active'

    @property
    def is_on(self) -> bool:
        return self._device.is_overrule_active

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_turn_on(self, **kwargs):
        self._device.set_overrule_active(self._gateway, True)
        self.on_change()

    async def async_turn_off(self, **kwargs):
        self._device.set_overrule_active(self._gateway, False)
        self.on_change()
