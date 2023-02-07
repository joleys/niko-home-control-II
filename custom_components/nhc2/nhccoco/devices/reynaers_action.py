from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_ACTION, PROPERTY_STATUS
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoReynaersAction(CoCoDevice):
    @property
    def action(self) -> str:
        return self.extract_property_value(PROPERTY_ACTION)

    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def possible_statuses(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_STATUS)

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def set_action(self, gateway, action: str):
        gateway.add_device_control(self.uuid, PROPERTY_ACTION, action)
