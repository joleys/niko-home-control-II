from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.generic_energyhome import CocoGenericEnergyhome
from .nhc_entity import NHCBaseEntity


class Nhc2GenericEnergyhomeElectricalPowerProductionThresholdExceededEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericEnergyhome, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_electrical_power_production_threshold_exceeded'

        self._attr_state = self._device.is_electrical_power_production_threshold_exceeded
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Electrical Power Production Threshold Exceeded'

    @property
    def is_on(self) -> bool:
        return self._device.is_electrical_power_production_threshold_exceeded
