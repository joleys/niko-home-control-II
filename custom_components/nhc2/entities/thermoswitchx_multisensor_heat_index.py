from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature

from ..nhccoco.devices.thermoswitchx_multisensor import CocoThermoswitchxMultisensor
from .nhc_entity import NHCBaseEntity


class Nhc2ThermoswitchxMultisensorHeatIndexEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoThermoswitchxMultisensor, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_heat_index'

        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_value = self._device.heat_index
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 0
        self._attr_native_precision = 0

    @property
    def name(self) -> str:
        return 'Heat Index'

    @property
    def native_value(self) -> int:
        return self._device.heat_index
