from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTemperature

from ..nhccoco.devices.virtual_hvac import CocoVirtualHvac


class Nhc2VirtualHvacOverruleSetpointEntity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoVirtualHvac, hub, gateway):
        """Initialize a temperature sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_overrule_setpoint'
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_value = self._device.overrule_setpoint
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_state_class = None
        self._attr_suggested_display_precision = 1
        self._attr_native_precision = 1

    @property
    def name(self) -> str:
        return 'Overrule Setpoint'

    @property
    def native_value(self) -> float:
        return self._device.overrule_setpoint

    def on_change(self):
        self.schedule_update_ha_state()
