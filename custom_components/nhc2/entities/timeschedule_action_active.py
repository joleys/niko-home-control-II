from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.timeschedule_action import CocoTimescheduleAction
from .nhc_entity import NHCBaseEntity


class Nhc2TimeschedulActionActiveEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoTimescheduleAction, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

        self._attr_state = self._device.is_active
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Active'

    @property
    def is_on(self) -> bool:
        return self._device.is_active
