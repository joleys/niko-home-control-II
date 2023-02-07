from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_ACTION
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoVeluxAction(CoCoDevice):
    @property
    def action(self) -> str:
        return self.extract_property_value(PROPERTY_ACTION)

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def set_action(self, gateway, action: str):
        gateway.add_device_control(self.uuid, PROPERTY_ACTION, action)
