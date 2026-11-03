from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.flux_fan import CocoFluxFan
from .nhc_entity import NHCBaseEntity


class Nhc2FluxFanFilterStatusEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoFluxFan, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_filter_status'

        self._attr_device_class = BinarySensorDeviceClass.PROBLEM
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Filter Cleaning Needed'

    @property
    def is_on(self) -> bool:
        return self._device.is_filter_cleaning_needed
