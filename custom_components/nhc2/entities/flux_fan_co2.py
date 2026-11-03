from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from ..nhccoco.devices.flux_fan import CocoFluxFan
from .nhc_entity import NHCBaseEntity


class Nhc2FluxFanCo2Entity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoFluxFan, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_co2'

        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = self._device.possible_co2

    @property
    def name(self) -> str:
        return 'CO2'

    @property
    def native_value(self) -> str:
        return self._device.co2
