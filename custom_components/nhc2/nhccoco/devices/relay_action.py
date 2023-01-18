from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoRelayAction(CoCoDevice):
    @property
    def status_status(self) -> str:
        return self.extract_property_value('Status')

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if 'Properties' in payload:
            self.merge_properties(payload['Properties'])

        if self._after_change_callback is not None:
            self._after_change_callback()
