from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.const import UnitOfTemperature

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit


class Nhc2GenericDomestichotwaterunitDomesticHotWaterTemperatureEntity(NumberEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericDomestichotwaterunit, hub, gateway):
        """Initialize a number entity."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_domestic_hot_water_temperature'
        self._attr_should_poll = False

        self._attr_device_class = NumberDeviceClass.TEMPERATURE
        min_value, max_value, step = self._device.domestic_hot_water_temperature_range
        self._attr_native_max_value = max_value
        self._attr_native_min_value = min_value
        self._attr_native_step = step
        self._attr_native_value = self._device.domestic_hot_water_temperature
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def name(self) -> str:
        return 'Domestic Hot Water Temperature'

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': f'{BRAND} ({self._device.technology})',
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        self._device.set_domestic_hot_water_temperature(self._gateway, value)
        self.on_change()
