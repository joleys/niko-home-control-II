from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTime

from ..nhccoco.devices.thermostat_thermostat import CocoThermostatThermostat
from .nhc_entity import NHCBaseEntity


class Nhc2ThermostatThermostatOverruleTimeEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoThermostatThermostat, hub, gateway):
        """Initialize a duration sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_overrule_time'

        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_native_value = self._device.overrule_time
        self._attr_native_unit_of_measurement = UnitOfTime.MINUTES

    @property
    def name(self) -> str:
        return 'Overrule Time'

    @property
    def native_value(self) -> int:
        return self._device.overrule_time
