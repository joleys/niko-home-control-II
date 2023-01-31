from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_ACTION, PROPERTY_ALIGNED, PROPERTY_ALIGNED_VALUE_TRUE, \
    PROPERTY_MOVING, PROPERTY_MOVING_VALUE_TRUE, PROPERTY_POSITION, PROPERTY_LAST_DIRECTION, PROPERTY_LAST_DIRECTION_VALUE_OPEN, PROPERTY_LAST_DIRECTION_VALUE_CLOSE
from ..helpers import to_int_or_none
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoMotorAction(CoCoDevice):
    @property
    def position(self) -> int:
        return to_int_or_none(self.extract_property_value(PROPERTY_POSITION))

    @property
    def aligned(self) -> str:
        return self.extract_property_value(PROPERTY_ALIGNED)

    @property
    def is_aligned(self) -> bool:
        return self.aligned == PROPERTY_ALIGNED_VALUE_TRUE

    @property
    def moving(self) -> str:
        return self.extract_property_value(PROPERTY_MOVING)

    @property
    def is_moving(self) -> bool:
        return self.moving == PROPERTY_MOVING_VALUE_TRUE

    @property
    def last_direction(self) -> str:
        return self.extract_property_value(PROPERTY_LAST_DIRECTION)

    @property
    def possible_last_directions(self) -> list:
        return [
            PROPERTY_LAST_DIRECTION_VALUE_OPEN,
            PROPERTY_LAST_DIRECTION_VALUE_CLOSE,
        ]

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def set_action(self, gateway, action: str):
        gateway.add_device_control(
            self.uuid,
            PROPERTY_ACTION,
            action
        )

    def set_position(self, gateway, position: int):
        gateway.add_device_control(
            self.uuid,
            PROPERTY_POSITION,
            position
        )
