import datetime
import logging

import json
from typing import List, Callable

import paho.mqtt.client as mqtt

from .nhc2light import NHC2Light
from .nhc2switch import NHC2Switch

TOPIC_SUFFIX_CMD = '/control/devices/cmd'
TOPIC_SUFFIX_RSP = '/control/devices/rsp'
TOPIC_SUFFIX_EVT = '/control/devices/evt'
TOPIC_PUBLIC_CMD = 'public/system/cmd'
TOPIC_PUBLIC_RSP = 'public/system/rsp'

TLS_VERSION = 2
MQTT_PROTOCOL = mqtt.MQTTv311
MQTT_TRANSPORT = "tcp"

_LOGGER = logging.getLogger(__name__)


class NHC2:
    def __init__(self, address, port, username, password, ca_path):
        client = mqtt.Client(protocol=MQTT_PROTOCOL, transport=MQTT_TRANSPORT)
        client.username_pw_set(username, password)
        client.tls_set(ca_path)
        client.tls_insecure_set(True)
        self._client = client
        self._address = address
        self._port = port
        self._profile_creation_id = username
        self._all_devices = None
        self._device_callbacks = None
        self._lights = None
        self._lights_callback: Callable[[List[NHC2Light]], None]
        self._switches = None
        self._switches_callback = Callable[[List[NHC2Switch]], None]
        self._system_info = None
        self._system_info_callback = Callable[[List[NHC2Switch]], None]
        self._lights_updates_callback = Callable[[List], None]
        self._switches_updates_callback = Callable[[List], None]

    def __del__(self):
        self._client.disconnect()

    def connect(self):

        def _on_message(client, userdata, message):
            _LOGGER.debug('GOT A MESSAGE')
            topic = message.topic
            response = json.loads(message.payload)
            if topic == TOPIC_PUBLIC_RSP and response['Method'] == 'systeminfo.publish':
                # Make sure we don't get a second response
                client.unsubscribe(TOPIC_PUBLIC_CMD)
                self._system_info = response
                self._system_info_callback(self._system_info)
            if topic == (self._profile_creation_id + TOPIC_SUFFIX_RSP):
                # Make sure we don't get a second response
                client.unsubscribe(self._profile_creation_id + TOPIC_SUFFIX_RSP)
                if response['Method'] == 'devices.list':
                    devices = self._get_devices(response)
                    self._device_callbacks = {x['Uuid']: {'callbackHolder': None} for x in devices}
                    lights = [x for x in devices if x['Model'] == 'light']
                    switches = [x for x in devices if x['Model'] == 'switched-generic']
                    self._lights = []
                    for light in lights:
                        self._lights.append(NHC2Light(light, self._device_callbacks[light['Uuid']], self._client, self._profile_creation_id))
                    self._switches = []
                    for switch in switches:
                        self._switches.append(NHC2Switch(switch, self._device_callbacks[switch['Uuid']], self._client, self._profile_creation_id))

                    self._lights_callback(self._lights)
                    self._switches_callback(self._lights)
                return
            if topic == (self._profile_creation_id + TOPIC_SUFFIX_EVT):
                if response['Method'] == 'devices.displayname_changed' or response['Method'] == 'devices.status' or \
                        response['Method'] == 'devices.changed' or response['Method'] == 'devices.param_changed' or \
                        response['Method'] == 'devices.added':
                    devices = self._get_devices(response)
                    for device in devices:
                        if self._device_callbacks and self._device_callbacks[device['Uuid']]:
                            self._device_callbacks[device['Uuid']]['callbackHolder'](device)
                return

        def _on_connect(client, userdata, flags, rc):
            client.subscribe(self._profile_creation_id + TOPIC_SUFFIX_RSP, qos=1)
            client.subscribe(TOPIC_PUBLIC_RSP, qos=1)
            client.subscribe(self._profile_creation_id + TOPIC_SUFFIX_EVT, qos=1)
            client.publish(TOPIC_PUBLIC_CMD, '{"Method":"systeminfo.publish"}', 1)
            client.publish(self._profile_creation_id + TOPIC_SUFFIX_CMD, '{"Method":"devices.list"}', 1)

        self._client.on_message = _on_message
        self._client.on_connect = _on_connect

        self._client.connect(self._address, self._port)
        _LOGGER.debug('NHC2 - Starting the loop')

        self._client.loop_start()

    def disconnect(self):
        self._client.loop_stop()
        self._client.disconnect()

    def _get_devices(self, response):
        params = response['Params']
        param_with_devices = next(filter((lambda x: x and 'Devices' in x), params), None)
        return param_with_devices['Devices']

    def get_systeminfo(self, callback):
        self._system_info_callback = callback
        if self._system_info:
            self._system_info_callback(self._system_info)

    def get_lights(self, callback):
        self._lights_callback = callback
        if self._lights:
            self._lights_callback(self._lights)

    def get_lights_updates(self, callback):
        self._lights_updates_callback = callback

    def get_switches(self, callback):
        self._switches_callback = callback
        if self._switches:
            self._switches_callback(self._switches)

    def get_switches_updates(self, callback):
        self._switches_updates_callback = callback

    def _emit_switches(self):
        self._switches_callback(self._switches)

