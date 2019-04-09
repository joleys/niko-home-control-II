from .nhc2entity import NHC2Entity
import json
import logging

TOPIC_SUFFIX_CMD = '/control/devices/cmd'

_LOGGER = logging.getLogger(__name__)


class NHC2Light(NHC2Entity):
    def __init__(self, dev, callbackContainer, client, profile_creation_id):
        super().__init__(dev, callbackContainer, client, profile_creation_id)
        self.update_dev(dev, callbackContainer)
        _LOGGER.debug('Setup of NHC2 switch device %s with name %s completed.', self.uuid, self.name)

    @property
    def is_on(self):
        return self._state

    def turn_on(self):
        self._change_status('On')

    def turn_off(self):
        self._change_status('Off')

    def update_dev(self, dev, callbackContainer=None):
        has_changed = super().update_dev(dev, callbackContainer)
        status_object = self._extract_status_object(dev)
        if self._check_for_status_change(status_object):
            self._state = self._status_prop_in_object_is_On(status_object)
            has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()

    def _extract_status_object(self, dev):
        if dev and 'Properties' in dev:
            properties = dev['Properties']
            if properties:
                return next(filter((lambda x: x and 'Status' in x), properties), None)
            else:
                return None
        else:
            return None

    def _status_prop_in_object_is_On(self, property_object_with_status):
        return property_object_with_status['Status'] == 'On'

    def _check_for_status_change(self, property_object_with_status):
        return property_object_with_status \
               and 'Status' in property_object_with_status \
               and self._state != (self._status_prop_in_object_is_On(property_object_with_status))

    def _change_status(self, status: str):
        command = {"Method": "devices.control", "Params": [
            {"Devices": [{"Properties": [{"Status": status}], "Uuid": self._uuid}]}
        ]}
        self._client.publish(self._profile_creation_id + TOPIC_SUFFIX_CMD, json.dumps(command), 1)
