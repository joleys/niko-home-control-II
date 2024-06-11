from homeassistant.components.binary_sensor import BinarySensorEntity

from ..nhccoco.devices.alloff_action import CocoAlloffAction
from .nhc_entity import NHCBaseEntity


class Nhc2AlloffActionStartedEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoAlloffAction, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_started'
        self._attr_state = self._device.is_all_started

    @property
    def name(self) -> str:
        return 'All Started'

    @property
    def is_on(self) -> bool:
        return self._device.is_all_started
