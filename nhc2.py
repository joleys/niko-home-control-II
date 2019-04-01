"""
Example of a custom MQTT component.

Shows how to communicate with MQTT. Follows a topic on MQTT and updates the
state of an entity to the last message received on that topic.

Also offers a service 'set_state' that will publish a message on the topic that
will be passed via MQTT to our message received listener. Call the service with
example payload {"new_state": "some new state"}.

Configuration:

To use the mqtt_example component you will need to add the following to your
configuration.yaml file.

mqtt_basic:
  topic: "home-assistant/mqtt_example"
"""

import logging

from homeassistant.components import mqtt
from homeassistant.components.light import ATTR_BRIGHTNESS, Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_PROFILE_CREATION_ID
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import json

# List of component names (string) your component depends upon.
DEPENDENCIES = ['mqtt']

TOPIC_SUFFIX_CMD = '/control/devices/cmd'
TOPIC_SUFFIX_RSP = '/control/devices/rsp'
TOPIC_SUFFIX_EVT = '/control/devices/evt'

CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_PROFILE_CREATION_ID): cv.string
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the MQTT example component."""
    profileCreationId = config.get(CONF_PROFILE_CREATION_ID)
    topicCmd = profileCreationId + TOPIC_SUFFIX_CMD
    topicRsp = profileCreationId + TOPIC_SUFFIX_RSP
    topicEvt = profileCreationId + TOPIC_SUFFIX_EVT

    mqtt.publish(hass, topicCmd, '{"Method":"devices.list"}')

    # Listen to a message on MQTT.
    def message_received(topicRsp, payload, qos):
        response = json.load(payload)
        if response.Method == 'devices.list':
            devices = response.Params[0].Devices
            lights = [x for x in devices if x.Model == 'light']
            # Add devices
            add_devices(NHC2Light(light, hass, topicCmd) for light in lights)
            # Return boolean to indicate that initialization was successfully.
            return True

    mqtt.subscribe(hass, topicRsp, message_received)


class NHC2Light(Light):
    """Representation of an Awesome Light."""

    def __init__(self, light, hass, topicCmd):
        """Initialize an AwesomeLight."""
        self._hass = hass
        self._topicCmd = topicCmd
        self._light = light
        self._name = light.Name
        self._state = light.Properties[0].Status == 'Off'
        self._brightness = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        command = {
            "Method": "devices.control",
            "Params": [
                {
                    "Devices": [
                        {
                            "Properties": [
                                {
                                    "Status": "On"
                                }
                            ],
                            "Uuid": self._light.Uuid
                        }
                    ]
                }
            ]
        }
        mqtt.publish(self._hass, self._topicCmd, json.dumps(command))

    def turn_off(self, **kwargs):
        command = {
            "Method": "devices.control",
            "Params": [
                {
                    "Devices": [
                        {
                            "Properties": [
                                {
                                    "Status": "Off"
                                }
                            ],
                            "Uuid": self._light.Uuid
                        }
                    ]
                }
            ]
        }
        mqtt.publish(self._hass, self._topicCmd, json.dumps(command))
