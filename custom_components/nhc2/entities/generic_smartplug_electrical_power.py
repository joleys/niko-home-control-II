from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfPower

from ..nhccoco.devices.generic_smartplug import CocoGenericSmartplug
from .nhc_entity import NHCBaseEntity


class Nhc2GenericSmartplugElectricalPowerEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericSmartplug, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid + '_electrical_power'

        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_native_value = self._device.electrical_power
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 3
        self._attr_native_precision = 3

    @property
    def name(self) -> str:
        return 'Electrical Power'

    @property
    def native_value(self) -> float:
        return self._device.electrical_power
