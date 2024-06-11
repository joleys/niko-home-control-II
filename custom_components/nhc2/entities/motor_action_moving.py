from homeassistant.components.binary_sensor import BinarySensorEntity

from ..nhccoco.devices.motor_action import CocoMotorAction
from .nhc_entity import NHCBaseEntity


class Nhc2MotorActionMovingEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoMotorAction, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_moving'
        self._attr_state = self._device.is_moving

    @property
    def name(self) -> str:
        return 'Moving'

    @property
    def is_on(self) -> bool:
        return self._device.is_moving
