from ..const import MQTT_DATA_METHOD, MQTT_DATA_METHOD_DEVICES_LIST, MQTT_TOPIC_SUFFIX_RSP

from datetime import datetime
import logging

_LOGGER = logging.getLogger(__name__)


class CocoController:
    def __init__(self):
        self._after_change_callbacks = []
        self._first_time_devices_list_received = None
        self._last_time_devices_list_received = None

    @property
    def first_time_device_list_received(self) -> datetime:
        return self._first_time_devices_list_received

    @property
    def last_time_device_list_received(self) -> datetime:
        return self._last_time_devices_list_received

    @property
    def after_change_callbacks(self):
        return self._after_change_callbacks

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'Controller changed ({topic} == {MQTT_TOPIC_SUFFIX_RSP}).')
        if topic.endswith(MQTT_TOPIC_SUFFIX_RSP) and payload[MQTT_DATA_METHOD] == MQTT_DATA_METHOD_DEVICES_LIST:
            self._last_time_devices_list_received = datetime.now()
            if self._first_time_devices_list_received is None:
                self._first_time_devices_list_received = self._last_time_devices_list_received

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def set_disconnected(self):
        return
