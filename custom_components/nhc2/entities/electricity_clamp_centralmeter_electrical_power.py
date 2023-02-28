from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfPower

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter


class Nhc2ElectricityClampCentralmeterElectricalPowerEntity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoElectricityClampCentralmeter, hub, gateway):
        """Initialize a sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_electrical_power'
        self._attr_should_poll = False

        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_native_value = self._device.electrical_power
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 0

    @property
    def name(self) -> str:
        return 'Electrical Power'

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': BRAND,
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def state(self) -> float:
        return self._device.electrical_power

    def on_change(self):
        self.schedule_update_ha_state()
