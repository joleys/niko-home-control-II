from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.generic_energyhome import CocoGenericEnergyhome

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2GenericEnergyhomeElectricalPowerProductionThresholdExceededEntity(BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericEnergyhome, hub, gateway):
        """Initialize a binary sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_electrical_power_production_threshold_exceeded'
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

        self._attr_state = self._device.is_electrical_power_production_threshold_exceeded
        self._attr_state_class = None
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Electrical Power Production Threshold Exceeded'

    @property
    def is_on(self) -> bool:
        return self._device.is_electrical_power_production_threshold_exceeded

    def on_change(self):
        self.schedule_update_ha_state()
