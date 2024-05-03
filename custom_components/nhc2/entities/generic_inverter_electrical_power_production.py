from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfPower

from ..nhccoco.devices.generic_inverter import CocoGenericInverter


class Nhc2GenericInverterElectricalPowerProductionEntity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericInverter, hub, gateway):
        """Initialize a sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_electrical_power_production'
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_native_value = self._device.electrical_power_production
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 3
        self._attr_native_precision = 3

    @property
    def name(self) -> str:
        return 'Electrical Power Production'

    @property
    def native_value(self) -> float:
        return self._device.electrical_power_production

    def on_change(self):
        self.schedule_update_ha_state()