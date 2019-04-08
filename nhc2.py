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
TOPIC_SUFFIX_SYS_EVT = '/system/evt'
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
        self._device_callbacks = {}
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
            topic = message.topic
            response = json.loads(message.payload)
            if topic == TOPIC_PUBLIC_RSP and response['Method'] == 'systeminfo.publish':
                self._system_info = response
                self._system_info_callback(self._system_info)
                return
            if topic == (self._profile_creation_id + TOPIC_SUFFIX_RSP):
                if response['Method'] == 'devices.list':
                    client.unsubscribe(self._profile_creation_id + TOPIC_SUFFIX_RSP)
                    devices = self._get_devices(response)
                    existing_uuids = list(self._device_callbacks.keys())
                    _LOGGER.debug("Existing UUIDs count: "+str(len(existing_uuids)))
                    _LOGGER.debug("Existing UUIDs: "+json.dumps(existing_uuids))

                    for x in devices:
                        if x['Uuid'] not in existing_uuids:
                            self._device_callbacks[x['Uuid']] = {'callbackHolder': None, 'entity': None}
                            _LOGGER.debug('Creating new callback for '+x['Name'])

                    lights = [x for x in devices if x['Model'] == 'light']
                    switches = [x for x in devices if x['Model'] == 'switched-generic']
                    _LOGGER.debug("New Lights count: "+str(len(lights)))
                    _LOGGER.debug("New Switches count: "+str(len(switches)))

                    self._lights = []
                    for light in lights:
                        if self._device_callbacks[light['Uuid']] and self._device_callbacks[light['Uuid']]['entity'] and self._device_callbacks[light['Uuid']]['entity'].uuid:
                            _LOGGER.debug('updating existing light')
                            self._device_callbacks[light['Uuid']]['entity'].update_dev(light)
                        else:
                            _LOGGER.debug('creating new light')
                            self._device_callbacks[light['Uuid']]['entity'] = NHC2Light(light, self._device_callbacks[light['Uuid']], self._client, self._profile_creation_id)
                        _LOGGER.debug('appending light to list')
                        self._lights.append(self._device_callbacks[light['Uuid']]['entity'])
                    self._switches = []
                    for switch in switches:
                        if self._device_callbacks[switch['Uuid']] and self._device_callbacks[switch['Uuid']]['entity'] and \
                                self._device_callbacks[switch['Uuid']]['entity'].uuid:
                            _LOGGER.debug('updating existing switch')
                            self._device_callbacks[switch['Uuid']]['entity'].update_dev(switch)
                        else:
                            _LOGGER.debug('creating new switch')
                            self._device_callbacks[switch['Uuid']]['entity'] = NHC2Switch(switch, self._device_callbacks[
                                switch['Uuid']], self._client, self._profile_creation_id)
                        _LOGGER.debug('appending switch to list')
                        self._switches.append(self._device_callbacks[switch['Uuid']]['entity'])

                    _LOGGER.debug("New Lights sent of count: "+str(len(self._lights)))
                    _LOGGER.debug("New Switches sent of count: "+str(len(self._switches)))

                    self._lights_callback(self._lights)
                    self._switches_callback(self._switches)
                return
            if topic == (self._profile_creation_id + TOPIC_SUFFIX_SYS_EVT) and response['Method'] == 'systeminfo.published':
                # If the connected controller publishes sysinfo... we expect something to have changed.
                _LOGGER.debug('NONO, we not know :)')
                client.subscribe(self._profile_creation_id + TOPIC_SUFFIX_RSP, qos=1)
                client.publish(self._profile_creation_id + TOPIC_SUFFIX_CMD, '{"Method":"devices.list"}')
                return
            if topic == (self._profile_creation_id + TOPIC_SUFFIX_EVT)\
               and (response['Method'] == 'devices.status' or response['Method'] == 'devices.changed'):
                _LOGGER.debug('Status Update')
                devices = self._get_devices(response)
                for device in devices:
                    if device['Uuid'] and self._device_callbacks[device['Uuid']]:
                        self._device_callbacks[device['Uuid']]['callbackHolder'](device)

                return

        def _on_connect(client, userdata, flags, rc):
            client.subscribe(self._profile_creation_id + TOPIC_SUFFIX_RSP, qos=1)
            client.subscribe(TOPIC_PUBLIC_RSP, qos=1)
            client.subscribe(self._profile_creation_id + TOPIC_SUFFIX_EVT, qos=1)
            client.subscribe(self._profile_creation_id + TOPIC_SUFFIX_SYS_EVT, qos=1)
            client.publish(TOPIC_PUBLIC_CMD, '{"Method":"systeminfo.publish"}', 1)
            client.publish(self._profile_creation_id + TOPIC_SUFFIX_CMD, '{"Method":"devices.list"}', 1)

        self._client.on_message = _on_message
        self._client.on_connect = _on_connect

        self._client.connect(self._address, self._port)

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

