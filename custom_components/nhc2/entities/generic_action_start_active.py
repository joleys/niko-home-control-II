from homeassistant.components.binary_sensor import BinarySensorEntity

from ..nhccoco.devices.generic_action import CocoGenericAction
from .nhc_entity import NHCBaseEntity


class Nhc2GenericActionStartActiveEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericAction, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_start_active'

        self._attr_state = self._device.is_start_active

    @property
    def name(self) -> str:
        return 'Start Active'

    @property
    def is_on(self) -> bool:
        return self._device.is_start_active
