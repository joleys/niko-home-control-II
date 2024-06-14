from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfPower

from ..nhccoco.devices.generic_energyhome import CocoGenericEnergyhome
from .nhc_entity import NHCBaseEntity


class Nhc2GenericEnergyhomeElectricalPowerFromGridEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericEnergyhome, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_electrical_power_from_grid'

        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_native_value = self._device.electrical_power_from_grid
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 3
        self._attr_native_precision = 3

    @property
    def name(self) -> str:
        return 'Electrical Power from Grid'

    @property
    def native_value(self) -> float:
        return self._device.electrical_power_from_grid
