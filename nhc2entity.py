import threading

from abc import ABC, abstractmethod


class NHC2Entity(ABC):

    @property
    def uuid(self):
        return self._uuid

    @property
    def name(self):
        return self._name

    @property
    def online(self):
        return self._online

    @property
    def model(self):
        return self._model

    @property
    def type(self):
        return self._type

    @property
    def profile_creation_id(self):
        return self._profile_creation_id

    @property
    def on_change(self):
        return self._on_change

    @on_change.setter
    def on_change(self, func):
        with self._callback_mutex:
            self._on_change = func

    def __init__(self, dev, callbackContainer, client, profile_creation_id):
        self._client = client
        self._profile_creation_id = profile_creation_id
        self._uuid = dev['Uuid']
        self._name = None
        self._online = None
        self._model = None
        self._type = None
        self._state = None
        self._callback_mutex = threading.RLock()
        self._on_state_change = None
        self._callback_mutex = threading.RLock()
        self._on_change = None
        self._callback_container = None
        self._after_update_callback = None

    def update_dev(self, dev, callback_container=None):
        has_changed = False
        if 'Name' in dev and self._name != dev['Name']:
            self._name = dev['Name']
            has_changed = True
        if 'DisplayName' in dev and self._name != dev['DisplayName']:
            self._name = dev['DisplayName']
            has_changed = True
        if 'Online' in dev and self._online != (dev['Online'] == 'True'):
            self._online = dev['Online'] == 'True'
            has_changed = True
        if 'Model' in dev and self._model != dev['Model']:
            self._model = dev['Model']
            has_changed = True
        if 'Type' in dev and self._type != dev['Type']:
            self._type = dev['Type']
            has_changed = True
        if callback_container:
            self._callback_container = callback_container
            if 'callbackHolder' in self._callback_container:
                self._callback_container['callbackHolder'] = self._update
                has_changed = True
        return has_changed

    @abstractmethod
    def _update(self, dev):
        pass

    def _state_changed(self):
        self.on_change()

