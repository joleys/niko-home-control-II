import os
import ssl
import uuid
import logging
import paho.mqtt.client as mqtt
from .const import MQTT_PROTOCOL, MQTT_TRANSPORT, MQTT_CERT_FILE

_LOGGER = logging.getLogger(__name__)

def create_ssl_context():
    context = ssl.create_default_context()
    ca_path = os.path.dirname(os.path.realpath(__file__)) + MQTT_CERT_FILE
    context.load_verify_locations(ca_path)
    context.check_hostname = False
    return context

# Fix blocking load_verify_locations call in event loop
ssl_context = create_ssl_context()

class NHCMQTTClient():
    @staticmethod
    def create(username=None, password=None):
        client = mqtt.Client(client_id="homeassistant-" + str(uuid.uuid1()), protocol=MQTT_PROTOCOL,
                             transport=MQTT_TRANSPORT)
        client.enable_logger(_LOGGER)
        if username != None or password != None:
            client.username_pw_set(username, password)
        client.tls_set_context(ssl_context)
        return client
