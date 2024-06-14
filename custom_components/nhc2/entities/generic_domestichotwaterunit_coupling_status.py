from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit
from .nhc_entity import NHCBaseEntity


class Nhc2GenericDomestichotwaterunitCouplingStatusEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericDomestichotwaterunit, hub, gateway):
        """Initialize a enum sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_coupling_status'

        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = self._device.possible_coupling_status
        self._attr_native_value = self._device.coupling_status
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Coupling Status'

    @property
    def state(self) -> str:
        return self._device.coupling_status
