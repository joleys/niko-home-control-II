from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature

from ..nhccoco.devices.thermoswitchx_multisensor import CocoThermoswitchxMultisensor
from .nhc_entity import NHCBaseEntity


class Nhc2ThermoswitchxMultisensorAmbientTemperatureEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoThermoswitchxMultisensor, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_ambient_temperature'

        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_value = self._device.ambient_temperature
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 1
        self._attr_native_precision = 1

    @property
    def name(self) -> str:
        return 'Ambient Temperature'

    @property
    def native_value(self) -> float:
        return self._device.ambient_temperature
