from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.const import UnitOfTemperature

from ..nhccoco.devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit
from .nhc_entity import NHCBaseEntity


class Nhc2GenericDomestichotwaterunitDomesticHotWaterTemperatureEntity(NHCBaseEntity, NumberEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericDomestichotwaterunit, hub, gateway):
        """Initialize a number entity."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_domestic_hot_water_temperature'

        self._attr_device_class = NumberDeviceClass.TEMPERATURE
        min_value, max_value, step = self._device.domestic_hot_water_temperature_range
        self._attr_native_max_value = max_value
        self._attr_native_min_value = min_value
        self._attr_native_step = step
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def name(self) -> str:
        return 'Domestic Hot Water Temperature'

    @property
    def native_value(self) -> float:
        return self._device.domestic_hot_water_temperature

    async def async_set_native_value(self, value: float) -> None:
        self._device.set_domestic_hot_water_temperature(self._gateway, value)
        self.schedule_update_ha_state()
