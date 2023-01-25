from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_ACTION, PROPERTY_ALIGNED, PROPERTY_ALIGNED_VALUE_TRUE, \
    PROPERTY_MOVING, \
    PROPERTY_MOVING_VALUE_TRUE, PROPERTY_POSITION
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoMotorAction(CoCoDevice):
    @property
    def status_position(self) -> int:
        return int(self.extract_property_value(PROPERTY_POSITION))

    @property
    def status_aligned(self) -> str:
        return self.extract_property_value(PROPERTY_ALIGNED)

    @property
    def is_aligned(self) -> bool:
        return self.status_aligned == PROPERTY_ALIGNED_VALUE_TRUE

    @property
    def status_moving(self) -> str:
        return self.extract_property_value(PROPERTY_MOVING)

    @property
    def is_moving(self) -> bool:
        return self.status_moving == PROPERTY_MOVING_VALUE_TRUE

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def set_action(self, gateway, action: str):
        gateway._add_device_control(
            self._device.uuid,
            PROPERTY_ACTION,
            action
        )

    def set_position(self, gateway, position: int):
        gateway._add_device_control(
            self._device.uuid,
            PROPERTY_POSITION,
            position
        )
