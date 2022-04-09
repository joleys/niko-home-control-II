import threading
from abc import ABC, abstractmethod

from .const import KEY_NAME, CALLBACK_HOLDER_PROP, KEY_TYPE, KEY_MODEL, KEY_ONLINE, KEY_DISPLAY_NAME
from .helpers import dev_prop_changed

class CoCoEntity(ABC):

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

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        self._client = client
        self._profile_creation_id = profile_creation_id
        self._uuid = dev['Uuid']
        self._name = None
        self._online = None
        self._model = None
        self._type = None
        self._command_device_control = command_device_control
        self._callback_mutex = threading.RLock()
        self._on_change = (lambda: print('%s (%s) has no _on_change callback set!' % (self._name, self._uuid)))
        self._callback_container = (
            lambda: print('%s (%s) has no _callback_container callback set!' % (self._name, self._uuid)))
        self._after_update_callback = (
            lambda: print('%s (%s) has no _after_update_callback callback set!' % (self._name, self._uuid)))

    def update_dev(self, dev, callback_container=None):
        has_changed = False
        if dev_prop_changed(self._name, dev, KEY_NAME):
            self._name = dev[KEY_NAME]
            has_changed = True
        if dev_prop_changed(self._name, dev, KEY_DISPLAY_NAME):
            self._name = dev[KEY_DISPLAY_NAME]
            has_changed = True
        if KEY_ONLINE in dev and self._online != (dev[KEY_ONLINE] == 'True'):
            self._online = dev[KEY_ONLINE] == 'True'
            has_changed = True
        if dev_prop_changed(self._model, dev, KEY_MODEL):
            self._model = dev[KEY_MODEL]
            has_changed = True
        if dev_prop_changed(self._type, dev, KEY_TYPE):
            self._type = dev[KEY_TYPE]
            has_changed = True
        if callback_container:
            self._callback_container = callback_container
            if CALLBACK_HOLDER_PROP in self._callback_container:
                self._callback_container[CALLBACK_HOLDER_PROP] = self._update
                has_changed = True
        return has_changed

    @abstractmethod
    def _update(self, dev):
        pass

    def _state_changed(self):
        self.on_change()
