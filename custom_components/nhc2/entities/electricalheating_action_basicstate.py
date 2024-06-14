from homeassistant.components.binary_sensor import BinarySensorEntity

from ..nhccoco.devices.electricalheating_action import CocoElectricalheatingAction
from .nhc_entity import NHCBaseEntity


class Nhc2ElectricalheatingActionBasicStateEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoElectricalheatingAction, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_basic_state'
        self._attr_state = self._device.is_basic_state_on

    @property
    def name(self) -> str:
        return 'Basic State'

    @property
    def is_on(self) -> bool:
        return self._device.is_basic_state_on
