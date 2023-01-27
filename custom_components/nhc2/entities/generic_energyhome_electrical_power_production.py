from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfPower

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.generic_energyhome import CocoGenericEnergyhome

class Nhc2GenericEnergyhomeElectricalPowerProductionEntity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericEnergyhome, hub, gateway):
        """Initialize a binary sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_electrical_power_production'
        self._attr_should_poll = False

        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_native_value = self._device.electrical_power_production
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self) -> str:
        return 'Electrical Power Production'

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
        return self._device.electrical_power_production

    def on_change(self):
        self.schedule_update_ha_state()
