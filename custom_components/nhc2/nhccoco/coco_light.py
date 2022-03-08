import logging

from .coco_entity import CoCoEntity
from .const import KEY_STATUS, VALUE_ON, VALUE_OFF, KEY_BRIGHTNESS, VALUE_DIMMER
from .helpers import extract_property_value_from_device

_LOGGER = logging.getLogger(__name__)


class CoCoLight(CoCoEntity):

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @property
    def support_brightness(self):
        return self._model == VALUE_DIMMER

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._is_on = None
        self._brightness = None
        self.update_dev(dev, callback_container)

    def turn_on(self):
        self._command_device_control(self._uuid, KEY_STATUS, VALUE_ON)

    def turn_off(self):
        self._command_device_control(self._uuid, KEY_STATUS, VALUE_OFF)

    def set_brightness(self, brightness):
        if brightness == brightness and 100 >= brightness >= 0:
            self._command_device_control(self._uuid, KEY_BRIGHTNESS, str(brightness))
        else:
            _LOGGER.error('Invalid brightness value passed. Must be integer [0-100]')

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        status_value = extract_property_value_from_device(dev, KEY_STATUS)
        if status_value and self._is_on != (status_value == VALUE_ON):
            self._is_on = (status_value == VALUE_ON)
            has_changed = True
        if self.support_brightness:
            brightness_value = extract_property_value_from_device(dev, KEY_BRIGHTNESS)
            if brightness_value is not None and self._brightness != int(brightness_value):
                self._brightness = int(brightness_value)
                has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()
