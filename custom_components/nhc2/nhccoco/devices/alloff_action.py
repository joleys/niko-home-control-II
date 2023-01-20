from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoAlloffAction(CoCoDevice):
    @property
    def status_basic_state(self) -> str:
        return self.extract_property_value('BasicState')

    @property
    def status_all_off_active(self) -> str:
        return self.extract_property_value('AllOffActive')

    @property
    def is_on(self) -> bool:
        return self.status_basic_state == 'On'

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if 'Properties' in payload:
            self.merge_properties(payload['Properties'])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def press(self, gateway):
        gateway._add_device_control(self._device.uuid, "BasicState", "Triggered")
