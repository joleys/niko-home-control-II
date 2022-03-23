from .coco_entity import CoCoEntity
from .const import ENERGY_POWER, ENERGY_REPORT
from .helpers import extract_property_value_from_device


class CoCoEnergyMeter(CoCoEntity):

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self.update_dev(dev, callback_container)
        self._command_device_control(self._uuid, ENERGY_REPORT, 'True')

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        status_value = extract_property_value_from_device(dev, ENERGY_POWER)
        if status_value:
            self._state = status_value
            has_changed = True
        status_value = extract_property_value_from_device(dev, ENERGY_REPORT)
        if status_value == 'False':
            self._command_device_control(self._uuid, ENERGY_REPORT, 'True')
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()

    @property
    def state(self):
        return self._state