import datetime

from .nhc2entity import NHC2Entity
import json
import logging

TOPIC_SUFFIX_CMD = '/control/devices/cmd'


class NHC2Light(NHC2Entity):
    def __init__(self, dev, callbackContainer, client, profile_creation_id):
        super().__init__(dev, callbackContainer, client, profile_creation_id)

    def _process_dev(self, dev, callbackContainer=None):
        has_changed = super()._process_dev(dev,callbackContainer)
        if self._uuid == dev['Uuid']:
            property_with_status = self.extract_status_property(dev)
            if property_with_status and 'Status' in property_with_status and \
                    self._state != (property_with_status['Status'] == 'On'):
                self._state = property_with_status['Status'] == 'On'
                has_changed = True
        return has_changed

    def _update(self, dev):
        has_changed = self._process_dev(dev)
        if has_changed:
            self._state_changed()

    def extract_status_property(self, dev):
        return next(filter((lambda x: x and 'Status' in x), dev['Properties']), None)

    def is_on(self):
        return self._state

    def turn_on(self):
        self._change_status('On')

    def turn_off(self):
        self._change_status('Off')

    def _change_status(self, status: str):
        command = {"Method": "devices.control", "Params": [
            {"Devices": [{"Properties": [{"Status": status}], "Uuid": self._uuid}]}
        ]}
        self._client.publish(self._profile_creation_id + TOPIC_SUFFIX_CMD, json.dumps(command), 1)
