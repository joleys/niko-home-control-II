import json
import asyncio

from .mqtt import NHCMQTTClient

from .const import MQTT_TOPIC_PUBLIC_AUTH_RSP, MQTT_TOPIC_PUBLIC_AUTH_CMD


class CoCoProfiles:
    """CoCoProfiles will collect a list of profiles on a NHC2
    """

    def __init__(self, address, port=8883):
        client = NHCMQTTClient.create()

        self._client = client
        self._address = address
        self._loop = 0
        self._max_loop = 200
        self._port = port
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._profiles = []

    async def get_all_profiles(self):
        self._client.connect_async(self._address, self._port)
        self._client.loop_start()
        while self._max_loop > self._loop >= 0:
            self._loop = self._loop + 1
            await asyncio.sleep(0.05)
        self._client.disconnect()
        return self._profiles

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(MQTT_TOPIC_PUBLIC_AUTH_RSP, qos=1)
            client.publish(MQTT_TOPIC_PUBLIC_AUTH_CMD, '{"Method":"profiles.list"}', 1)
        else:
            self._loop = -100

    def _on_message(self, client, userdata, message):
        topic = message.topic
        response = json.loads(message.payload)
        if topic == MQTT_TOPIC_PUBLIC_AUTH_RSP \
                and response.get('Method') == 'profiles.list' \
                and 'Params' in response \
                and (len(response.get('Params')) == 1) \
                and 'Profiles' in response.get('Params')[0]:
            self._profiles = response.get('Params')[0].get('Profiles')
            self._loop = -1
