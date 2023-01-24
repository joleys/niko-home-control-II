import json
import logging
import os
import threading
from time import sleep
from typing import Callable
import sys

import paho.mqtt.client as mqtt

from .coco_device_class import CoCoDeviceClass
from .coco_fan import CoCoFan
from .coco_switched_fan import CoCoSwitchedFan
from .coco_climate import CoCoThermostat
from .coco_energy import CoCoEnergyMeter
from .coco_cover import CoCoCover
from .coco_generic import CoCoGeneric

from .devices.accesscontrol_action import CocoAccesscontrolAction
from .devices.alloff_action import CocoAlloffAction
from .devices.dimmer_action import CocoDimmerAction
from .devices.light_action import CocoLightAction
from .devices.naso_smartplug import CocoNasoSmartplug
from .devices.socket_action import CocoSocketAction
from .devices.switched_fan_action import CocoSwitchedFanAction
from .devices.switched_generic_action import CocoSwitchedGenericAction

from .const import *
from .helpers import *

_LOGGER = logging.getLogger(__name__)
sem = threading.Semaphore()

DEVICE_SETS = {
    CoCoDeviceClass.SWITCHED_FANS: {INTERNAL_KEY_CLASS: CoCoSwitchedFan, INTERNAL_KEY_MODELS: LIST_VALID_SWITCHED_FANS},
    CoCoDeviceClass.FANS: {INTERNAL_KEY_CLASS: CoCoFan, INTERNAL_KEY_MODELS: LIST_VALID_FANS},
    CoCoDeviceClass.COVERS: {INTERNAL_KEY_CLASS: CoCoCover, INTERNAL_KEY_MODELS: LIST_VALID_COVERS},
    CoCoDeviceClass.SWITCHES: {INTERNAL_KEY_CLASS: CoCoSwitch, INTERNAL_KEY_MODELS: LIST_VALID_SWITCHES},
    CoCoDeviceClass.LIGHTS: {INTERNAL_KEY_CLASS: CoCoLight, INTERNAL_KEY_MODELS: LIST_VALID_LIGHTS},
    CoCoDeviceClass.THERMOSTATS: {INTERNAL_KEY_CLASS: CoCoThermostat, INTERNAL_KEY_MODELS: LIST_VALID_THERMOSTATS},
    CoCoDeviceClass.ENERGYMETERS: {INTERNAL_KEY_CLASS: CoCoEnergyMeter, INTERNAL_KEY_MODELS: LIST_VALID_ENERGYMETERS},
    CoCoDeviceClass.ACCESSCONTROL: {INTERNAL_KEY_CLASS: CoCoAccessControl,
                                    INTERNAL_KEY_MODELS: LIST_VALID_ACCESSCONTROL},
    CoCoDeviceClass.BUTTONS: {INTERNAL_KEY_CLASS: CoCoButton, INTERNAL_KEY_MODELS: LIST_VALID_BUTTONS},
    CoCoDeviceClass.SMARTPLUGS: {INTERNAL_KEY_CLASS: CoCoSmartPlug, INTERNAL_KEY_MODELS: LIST_VALID_SMARTPLUGS},
    CoCoDeviceClass.GENERIC: {INTERNAL_KEY_CLASS: CoCoGeneric, INTERNAL_KEY_MODELS: LIST_VALID_GENERICS}
}


class CoCo:
    def __init__(self, address, username, password, port=8884, ca_path=None, switches_as_lights=False):

        if switches_as_lights:
            DEVICE_SETS[CoCoDeviceClass.LIGHTS] = {INTERNAL_KEY_CLASS: CoCoLight,
                                                   INTERNAL_KEY_MODELS: LIST_VALID_LIGHTS + LIST_VALID_SWITCHES}
            DEVICE_SETS[CoCoDeviceClass.SWITCHES] = {INTERNAL_KEY_CLASS: CoCoSwitch, INTERNAL_KEY_MODELS: []}
        # The device control buffer fields
        self._keep_thread_running = True
        self._device_control_buffer = {}
        self._device_control_buffer_size = DEVICE_CONTROL_BUFFER_SIZE
        self._device_control_buffer_command_size = DEVICE_CONTROL_BUFFER_COMMAND_SIZE
        self._device_control_buffer_command_count = 0
        self._device_control_buffer_thread = threading.Thread(target=self._publish_device_control_commands)
        self._device_control_buffer_thread.start()

        if ca_path is None:
            ca_path = os.path.dirname(os.path.realpath(__file__)) + MQTT_CERT_FILE

        # Configure the client
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
        self._devices = {}
        self._devices_callback = {}
        self._system_info = None
        self._system_info_callback = lambda x: None
        self._device_instances = {}

    @property
    def address(self):
        return self._address

    def __del__(self):
        self._keep_thread_running = False
        self._client.disconnect()

    def connect(self):
        def _on_message(client, userdata, message):
            topic = message.topic
            response = json.loads(message.payload)

            # System info response (/system/rsp, method: systeminfo.publish)
            if topic == self._profile_creation_id + MQTT_TOPIC_PUBLIC_RSP and \
                    response[KEY_METHOD] == MQTT_METHOD_SYSINFO_PUBLISH:
                self._system_info = response
                self._system_info_callback(self._system_info)

            # Device list response (/control/devices/rsp, method: devices.list)
            elif topic == (self._profile_creation_id + MQTT_TOPIC_SUFFIX_RSP) and \
                    response[KEY_METHOD] == MQTT_METHOD_DEVICES_LIST:
                # No need to listen for devices anymore. So unsubscribe.
                self._client.unsubscribe(self._profile_creation_id + MQTT_TOPIC_SUFFIX_RSP)
                self._process_devices_list(response)

            # System info published (/system/evt, method: systeminfo.published)
            elif topic == (self._profile_creation_id + MQTT_TOPIC_SUFFIX_SYS_EVT) and \
                    response[KEY_METHOD] == MQTT_METHOD_SYSINFO_PUBLISHED:
                # If the connected controller publishes sysinfo we expect something to have changed.
                # So ask the list of devices again.
                # To be honest: I don't think this will do anything usefull, as no new entities will be created.
                client.subscribe(self._profile_creation_id + MQTT_TOPIC_SUFFIX_RSP, qos=1)
                client.publish(
                    self._profile_creation_id + MQTT_TOPIC_SUFFIX_CMD,
                    json.dumps({KEY_METHOD: MQTT_METHOD_DEVICES_LIST}),
                    1
                )

            # Device events (/control/devices/evt, method: devices.status or devices.changed)
            elif topic == (self._profile_creation_id + MQTT_TOPIC_SUFFIX_EVT) and (
                    response[KEY_METHOD] == MQTT_METHOD_DEVICES_STATUS or
                    response[KEY_METHOD] == MQTT_METHOD_DEVICES_CHANGED
            ):
                devices = extract_devices(response)

                for device in devices:
                    if KEY_UUID not in device:
                        continue

                    try:
                        self._device_instances[device[KEY_UUID]].on_change(topic, device)
                    except Exception as e:
                        _LOGGER.debug(f'Failed to invoke callback: {device[KEY_UUID]}. Topic: {topic} | Data: {device}')
                        pass

        def _on_connect(client, userdata, flags, rc):
            if rc == 0:
                _LOGGER.debug('Connected to MQTT broker')

                # Subscribe to the MQTT topics
                client.subscribe(self._profile_creation_id + MQTT_TOPIC_SUFFIX_RSP, qos=1)
                client.subscribe(self._profile_creation_id + MQTT_TOPIC_PUBLIC_RSP, qos=1)
                client.subscribe(self._profile_creation_id + MQTT_TOPIC_SUFFIX_EVT, qos=1)
                client.subscribe(self._profile_creation_id + MQTT_TOPIC_SUFFIX_SYS_EVT, qos=1)

                # ask the system information
                client.publish(
                    self._profile_creation_id + MQTT_TOPIC_PUBLIC_CMD,
                    json.dumps({KEY_METHOD: MQTT_METHOD_SYSINFO_PUBLISH}),
                    1
                )

                # ask the devices list
                client.publish(
                    self._profile_creation_id + MQTT_TOPIC_SUFFIX_CMD,
                    json.dumps({KEY_METHOD: MQTT_METHOD_DEVICES_LIST}),
                    1
                )
            elif MQTT_RC_CODES[rc]:
                raise Exception(MQTT_RC_CODES[rc])
            else:
                raise Exception('Unknown error')

        def _on_disconnect(client, userdata, rc):
            _LOGGER.warning('Disconnected from MQTT broker')
            for device in self._device_instances.values():
                device.is_online = False

        # Configure the callbacks
        self._client.on_message = _on_message
        self._client.on_connect = _on_connect
        self._client.on_disconnect = _on_disconnect

        self._client.connect_async(self._address, self._port)
        self._client.loop_start()

    def disconnect(self):
        self._client.loop_stop()
        self._client.disconnect()

    def get_systeminfo(self, callback):
        self._system_info_callback = callback
        if self._system_info:
            self._system_info_callback(self._system_info)

    def get_devices(self, device_class: CoCoDeviceClass, callback: Callable):
        self._devices_callback[device_class] = callback
        if self._devices and device_class in self._devices:
            self._devices_callback[device_class](self._devices[device_class])

    def get_device_instances(self, device_class):
        if len(self._device_instances) == 0:
            _LOGGER.warning(f'No devices yet, probably waiting for device list.')
            sleep(0.05)
            return self.get_device_instances(device_class)

        devices = []
        for device in self._device_instances.values():
            if isinstance(device, device_class):
                devices.append(device)

        return devices

    def _publish_device_control_commands(self):
        while self._keep_thread_running:
            device_commands_to_process = None
            sem.acquire()
            if len(self._device_control_buffer.keys()) > 0:
                device_commands_to_process = self._device_control_buffer
            self._device_control_buffer = {}
            self._device_control_buffer_command_count = 0
            sem.release()
            if device_commands_to_process is not None:
                command = process_device_commands(device_commands_to_process)
                self._client.publish(
                    self._profile_creation_id + MQTT_TOPIC_SUFFIX_CMD,
                    json.dumps(command),
                    1
                )
            sleep(0.05)

    def _add_device_control(self, uuid, property_key, property_value):
        while len(self._device_control_buffer.keys()) >= self._device_control_buffer_size or \
                self._device_control_buffer_command_count >= self._device_control_buffer_command_size:
            pass
        sem.acquire()
        self._device_control_buffer_command_count += 1
        if uuid not in self._device_control_buffer:
            self._device_control_buffer[uuid] = {}
        self._device_control_buffer[uuid][property_key] = property_value
        sem.release()

    def _process_devices_list(self, response):
        """Convert the response of devices.list into device instances."""
        devices = extract_devices(response)
        self._device_instances = self._convert_to_device_instances(devices)

        # for uuid, device in self._device_instances.items():
        #     self._device_callbacks[uuid] = device.on_change

        # Only add devices that are actionable
        # actionable_devices = list(
        #     filter(lambda d: d[KEY_TYPE] == DEV_TYPE_ACTION, extract_devices(response)))
        # actionable_devices.extend(list(
        #     filter(lambda d: d[KEY_TYPE] == "thermostat", extract_devices(response))))
        # actionable_devices.extend(list(
        #     filter(lambda d: d[KEY_TYPE] == "centralmeter", extract_devices(response))))
        # actionable_devices.extend(list(
        #     filter(lambda d: d[KEY_TYPE] == "smartplug", extract_devices(response))))

        # Only prepare for devices that don't already exist
        # # TODO - Can't we do this when we need it (in initialize_devices ?)
        # existing_uuids = list(self._device_callbacks.keys())
        # for actionable_device in actionable_devices:
        #     if actionable_device[KEY_UUID] not in existing_uuids:
        #         self._device_callbacks[actionable_device[KEY_UUID]] = \
        #             {INTERNAL_KEY_CALLBACK: None, KEY_ENTITY: None}

        # Initialize
        # self.initialize_devices(CoCoDeviceClass.SWITCHED_FANS, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.FANS, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.SWITCHES, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.LIGHTS, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.COVERS, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.THERMOSTATS, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.ENERGYMETERS, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.ACCESSCONTROL, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.BUTTONS, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.SMARTPLUGS, actionable_devices)
        # self.initialize_devices(CoCoDeviceClass.GENERIC, actionable_devices)

    def _convert_to_device_instances(self, devices: list):
        device_instances = {}
        for device in devices:
            try:
                classname = str.replace(
                    str.title(
                        str.replace(
                            'Coco ' + device["Model"] + ' ' + device["Type"],
                            '-',
                            ' '
                        )
                    ),
                    ' ',
                    ''
                )

                # ignore some devices
                if classname in [
                    # These are devices, but don't receive any events through MQTT. So we can't do anything with them.
                    'CocoDimcontrollerSmartpanel',
                    'CocoDimmerSmartdimmer',
                    'CocoExtensionbuttonx1Smartextensionpanel',
                    'CocoGenericBrick',
                    'CocoGenericGatewayfw',
                    'CocoGenericRadio',
                    'CocoGenericStick',
                    'CocoLightSmartrelay',
                    'CocoPushbuttonx1FeedbackSmartpanel',
                    'CocoPushbuttonx1Smartpanel',
                ]:
                    continue

                instance = getattr(sys.modules[__name__], classname)(json_to_map(device))
                self._device_instances[instance.uuid] = instance
            except Exception as e:
                _LOGGER.warning(f"Class {classname} not found {e}")
