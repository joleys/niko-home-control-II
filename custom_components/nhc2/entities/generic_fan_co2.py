from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import CONCENTRATION_PARTS_PER_MILLION

from ..nhccoco.devices.generic_fan import CocoGenericFan
from .nhc_entity import NHCBaseEntity


class Nhc2GenericFanCo2Entity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericFan, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_co2'

        self._attr_device_class = SensorDeviceClass.CO2
        self._attr_native_value = self._device.co2
        self._attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION
        self._attr_suggested_display_precision = 0
        self._attr_native_precision = 0

    @property
    def name(self) -> str:
        return 'CO2'

    @property
    def native_value(self) -> int:
        return self._device.co2
