from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.thermostat_hvac import CocoThermostatHvac


class Nhc2ThermostatHvacEcoSaveEntity(SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoThermostatHvac, hub, gateway):
        """Initialize a switch sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_ecosave'
        self._attr_should_poll = False
        self._attr_device_class = SwitchDeviceClass.SWITCH

    @property
    def name(self) -> str:
        return 'Thermostat EcoSave'

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': BRAND,
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def is_on(self) -> bool:
        return self._device.is_ecosave

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_turn_on(self, **kwargs):
        self._device.set_ecosave(self._gateway, True)
        self.on_change()

    async def async_turn_off(self, **kwargs):
        self._device.set_ecosave(self._gateway, False)
        self.on_change()
