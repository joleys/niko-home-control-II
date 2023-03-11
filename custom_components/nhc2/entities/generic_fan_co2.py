from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import CONCENTRATION_PARTS_PER_MILLION

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.generic_fan import CocoGenericFan


class Nhc2GenericFanCo2Entity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericFan, hub, gateway):
        """Initialize a sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_co2'
        self._attr_should_poll = False

        self._attr_device_class = SensorDeviceClass.CO2
        self._attr_native_value = self._device.co2
        self._attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION
        self._attr_state_class = None
        self._attr_suggested_display_precision = 0

    @property
    def name(self) -> str:
        return 'CO2'

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': f'{BRAND} ({self._device.technology})',
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def state(self) -> int:
        return self._device.co2

    def on_change(self):
        self.schedule_update_ha_state()
