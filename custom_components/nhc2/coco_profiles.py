import json
import os
from time import sleep

import paho.mqtt.client as mqtt

from .const import MQTT_TOPIC_PUBLIC_AUTH_RSP, MQTT_PROTOCOL, MQTT_TRANSPORT, MQTT_TOPIC_PUBLIC_AUTH_CMD


class CoCoProfiles:
    """CoCoDiscover will collect a list of profiles on a NHC2
    """

    def __init__(self, callback, address, done_discovering_profiles_callback, port=8883, ca_path=None):

        if ca_path is None:
            ca_path = os.path.dirname(os.path.realpath(__file__)) + '/coco_ca.pem'
        client = mqtt.Client(protocol=MQTT_PROTOCOL, transport=MQTT_TRANSPORT)
        client.tls_set(ca_path)
        client.tls_insecure_set(True)
        self._client = client
        self._address = address
        self._callback = callback
        self._done_discovering_profiles_callback = done_discovering_profiles_callback
        self._loop = 0
        self._max_loop = 200
        self._port = port
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.connect_async(self._address, self._port)
        self._client.loop_start()
        while self._max_loop > self._loop >= 0:
            self._loop = self._loop + 1
            sleep(0.05)
        if self._loop > 0:
            self._callback(None)
        self._done_discovering_profiles_callback()
        self._client.disconnect()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(MQTT_TOPIC_PUBLIC_AUTH_RSP, qos=1)
            client.publish(MQTT_TOPIC_PUBLIC_AUTH_CMD, '{"Method":"profiles.list"}', 1)
        else:
            self._callback([])
            self._loop = -100

    def _on_message(self, client, userdata, message):

        topic = message.topic
        response = json.loads(message.payload)
        if topic == MQTT_TOPIC_PUBLIC_AUTH_RSP \
                and response.get('Method') == 'profiles.list' \
                and 'Params' in response \
                and (len(response.get('Params')) == 1) \
                and 'Profiles' in response.get('Params')[0]:
            self._loop = -1
            self._callback(response.get('Params')[0].get('Profiles'))
