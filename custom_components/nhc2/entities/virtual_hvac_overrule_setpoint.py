from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTemperature

from ..nhccoco.devices.virtual_hvac import CocoVirtualHvac
from .nhc_entity import NHCBaseEntity


class Nhc2VirtualHvacOverruleSetpointEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoVirtualHvac, hub, gateway):
        """Initialize a temperature sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_overrule_setpoint'

        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_value = self._device.overrule_setpoint
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_suggested_display_precision = 1
        self._attr_native_precision = 1

    @property
    def name(self) -> str:
        return 'Overrule Setpoint'

    @property
    def native_value(self) -> float:
        return self._device.overrule_setpoint
