from homeassistant.components.binary_sensor import BinarySensorEntity

from ..nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac


class Nhc2HvacthermostatHvacHvacOnEntity(BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoHvacthermostatHvac, hub, gateway):
        """Initialize a switch sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_hvac_on'
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

    @property
    def name(self) -> str:
        return 'HVAC on'

    @property
    def is_on(self) -> bool:
        return self._device.is_hvac_on

    def on_change(self):
        self.schedule_update_ha_state()
