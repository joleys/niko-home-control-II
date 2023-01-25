from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import TIME_MINUTES

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac


class Nhc2HvacthermostatHvacOverruleTimeEntity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoHvacthermostatHvac, hub, gateway):
        """Initialize a temperature sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_hvacthermostat_overrule_time'
        self._attr_should_poll = False

        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_native_value = self._device.status_overrule_time
        self._attr_native_unit_of_measurement = TIME_MINUTES
        self._attr_state_class = None

    @property
    def name(self) -> str:
        return 'HVAC Thermostat Overrule time'

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

    def on_change(self):
        self.schedule_update_ha_state()
