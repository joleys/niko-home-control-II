from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.generic_chargingstation import CocoGenericChargingstation
from .nhc_entity import NHCBaseEntity


class Nhc2GenericChargingstationTargetReachedEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericChargingstation, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_target_reached'

        self._attr_state = self._device.is_target_reached

    @property
    def name(self) -> str:
        return 'Target Reached'

    @property
    def is_on(self) -> bool:
        return self._device.is_target_reached
