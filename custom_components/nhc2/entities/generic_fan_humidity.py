from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import PERCENTAGE

from ..nhccoco.devices.generic_fan import CocoGenericFan
from .nhc_entity import NHCBaseEntity


class Nhc2GenericFanHumidityEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericFan, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_humidity'

        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_native_value = self._device.humidity
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_suggested_display_precision = 0
        self._attr_native_precision = 0

    @property
    def name(self) -> str:
        return 'Humidity'

    @property
    def native_value(self) -> int:
        return self._device.humidity
