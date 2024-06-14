from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from ..nhccoco.devices.motor_action import CocoMotorAction
from .nhc_entity import NHCBaseEntity


class Nhc2MotorActionLastDirectionEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoMotorAction, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_last_direction'

        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = self._device.possible_last_directions
        self._attr_native_value = self._device.last_direction

    @property
    def name(self) -> str:
        return 'Last Direction'

    @property
    def state(self) -> str:
        return self._device.last_direction
