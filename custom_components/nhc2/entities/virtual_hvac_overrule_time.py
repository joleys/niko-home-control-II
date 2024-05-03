from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTime

from ..nhccoco.devices.virtual_hvac import CocoVirtualHvac


class Nhc2VirtualHvacOverruleTimeEntity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoVirtualHvac, hub, gateway):
        """Initialize a duration sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_overrule_time'
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_native_value = self._device.overrule_time
        self._attr_native_unit_of_measurement = UnitOfTime.MINUTES
        self._attr_state_class = None

    @property
    def name(self) -> str:
        return 'Overrule time'

    @property
    def native_value(self) -> int:
        return self._device.overrule_time

    def on_change(self):
        self.schedule_update_ha_state()
