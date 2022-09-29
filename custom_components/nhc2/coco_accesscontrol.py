import logging

from custom_components.nhc2.coco_entity import CoCoEntity

_LOGGER = logging.getLogger(__name__)

class CoCoAccessControl(CoCoEntity):

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self.update_dev(dev, callback_container)

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()

    @property
    def stream_source(self):
        return 'http://192.168.0.1:15110'

    @property
    def username(self):
        return 'user'

    @property
    def password(self):
        return ''
