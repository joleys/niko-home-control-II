from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass

from ..nhccoco.devices.garagedoor_action import CocoGaragedoorAction
from .nhc_entity import NHCBaseEntity


class Nhc2GaragedoorActionPortClosedEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGaragedoorAction, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_port_closed'

        self._attr_state = self._device.is_port_open
        self._attr_device_class = BinarySensorDeviceClass.GARAGE_DOOR

    @property
    def name(self) -> str:
        return 'Port Closed'

    @property
    def is_on(self) -> bool:
        return self._device.is_port_open
