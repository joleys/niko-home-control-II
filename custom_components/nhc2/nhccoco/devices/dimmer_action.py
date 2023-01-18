from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoDimmerAction(CoCoDevice):
    @property
    def status_status(self) -> str:
        return self.extract_property_value('Status')

    @property
    def status_brightness(self) -> int:
        return int(self.extract_property_value('Brightness'))

    @property
    def status_aligned(self) -> bool:
        return self.extract_property_value('Aligned') == 'True'

    @property
    def is_on(self) -> bool:
        return self.status_status == 'On'

    @property
    def support_brightness(self) -> bool:
        return True

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if 'Properties' in payload:
            self.merge_properties(payload['Properties'])

        if self._after_change_callback is not None:
            self._after_change_callback()
