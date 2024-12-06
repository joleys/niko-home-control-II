import json
import os
import threading
from time import sleep
import sys
import uuid

import paho.mqtt.client as mqtt

from .devices.accesscontrol_action import CocoAccesscontrolAction
from .devices.airco_hvac import CocoAircoHvac
from .devices.alarms_action import CocoAlarmsAction
from .devices.alloff_action import CocoAlloffAction
from .devices.audiocontrol_action import CocoAudiocontrolAction
from .devices.bellbutton_action import CocoBellbuttonAction
from .devices.comfort_action import CocoComfortAction
from .devices.condition_action import CocoConditionAction
from .devices.controller import CocoController
from .devices.dimmer_action import CocoDimmerAction
from .devices.easee_chargingstation import CocoEaseeChargingstation
from .devices.electricalheating_action import CocoElectricalheatingAction
from .devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .devices.eve_chargingstation import CocoEveChargingstation
from .devices.fan_action import CocoFanAction
from .devices.flag_action import CocoFlagAction
from .devices.flag_virtual import CocoFlagVirtual
from .devices.garagedoor_action import CocoGaragedoorAction
from .devices.gate_action import CocoGateAction
from .devices.generic_action import CocoGenericAction
from .devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit
from .devices.generic_energyhome import CocoGenericEnergyhome
from .devices.generic_fan import CocoGenericFan
from .devices.generic_hvac import CocoGenericHvac
from .devices.generic_inverter import CocoGenericInverter
from .devices.generic_smartplug import CocoGenericSmartplug
from .devices.heatingcooling_action import CocoHeatingcoolingAction
from .devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .devices.light_action import CocoLightAction
from .devices.naso_smartplug import CocoNasoSmartplug
from .devices.overallcomfort_action import CocoOverallcomfortAction
from .devices.pir_action import CocoPirAction
from .devices.peakmode_action import CocoPeakmodeAction
from .devices.playerstatus_action import CocoPlayerstatusAction
from .devices.reynaers_action import CocoReynaersAction
from .devices.robinsip_videodoorstation import CocoRobinsipVideodoorstation
from .devices.rolldownshutter_action import CocoRolldownshutterAction
from .devices.simulation_action import CocoSimulationAction
from .devices.socket_action import CocoSocketAction
from .devices.sunblind_action import CocoSunblindAction
from .devices.switched_fan_action import CocoSwitchedFanAction
from .devices.switched_generic_action import CocoSwitchedGenericAction
from .devices.thermostat_hvac import CocoThermostatHvac
from .devices.thermostat_hvac_zigbee import CocoThermostatHvacZigbee
from .devices.thermostat_thermostat import CocoThermostatThermostat
from .devices.thermoswitchx_multisensor import CocoThermoswitchxMultisensor
from .devices.thermoswitchx1_multisensor import CocoThermoswitchx1Multisensor
from .devices.thermoswitchx1feedback_multisensor import CocoThermoswitchx1FeedbackMultisensor
from .devices.thermoswitchx2feedback_multisensor import CocoThermoswitchx2FeedbackMultisensor
from .devices.thermoswitchx4feedback_multisensor import CocoThermoswitchx4FeedbackMultisensor
from .devices.thermoswitchx6feedback_multisensor import CocoThermoswitchx6FeedbackMultisensor
from .devices.thermoventilationcontrollerfeedback_multisensor import CocoThermoventilationcontrollerfeedbackMultisensor
from .devices.timeschedule_action import CocoTimescheduleAction
from .devices.touchswitch_hvac import CocoTouchswitchHvac
from .devices.velux_action import CocoVeluxAction
from .devices.venetianblind_action import CocoVenetianblindAction
from .devices.virtual_hvac import CocoVirtualHvac
from .devices.virtual_thermostat import CocoVirtualThermostat

from .const import *
from .helpers import *

import logging

_LOGGER = logging.getLogger(__name__)
sem = threading.Semaphore()


class CoCo:
    def __init__(self, address, username, password, port=8884, ca_path=None):
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
        client = mqtt.Client(client_id="homeassistant-" + str(uuid.uuid1()), protocol=MQTT_PROTOCOL,
                             transport=MQTT_TRANSPORT)
        client.username_pw_set(username, password)
        client.tls_set(ca_path)
        client.tls_insecure_set(True)

        self._client = client
        self._address = address
        self._port = port
        self._profile_creation_id = username
        self._system_info_callback = lambda x: None
        self._devices_list_callback = lambda x: None
        self._device_instances = {
            'controller': CocoController()
        }
        self._entries_initialized = False

    @property
    def entries_initialized(self):
        return self._entries_initialized

    @property
    def address(self):
        return self._address

    def __del__(self):
        self._keep_thread_running = False
        self._client.disconnect()

    def connect(self, on_connection_refused=None):
        def _on_message(client, userdata, message):
            topic = message.topic
            response = json.loads(message.payload)

            # System info response (/system/rsp, method: systeminfo.publish)
            if topic == self._profile_creation_id + MQTT_TOPIC_PUBLIC_RSP and \
                    response[MQTT_DATA_METHOD] == MQTT_DATA_METHOD_SYSINFO_PUBLISH:
                self._system_info_callback(response)

            # Device list response (/control/devices/rsp, method: devices.list)
            elif topic == (self._profile_creation_id + MQTT_TOPIC_SUFFIX_RSP) and \
                    (response[MQTT_DATA_METHOD] == MQTT_DATA_METHOD_DEVICES_LIST):
                # No need to listen for devices anymore. So unsubscribe.
                self._client.unsubscribe(self._profile_creation_id + MQTT_TOPIC_SUFFIX_RSP)
                if self._process_devices_list(response):
                    self._device_instances['controller'].on_change(topic, response)
                    if self._devices_list_callback:
                        self._devices_list_callback()
                        self._entries_initialized = True

            # System info published (/system/evt, method: systeminfo.published)
            elif topic == (self._profile_creation_id + MQTT_TOPIC_SUFFIX_SYS_EVT) and \
                    response[MQTT_DATA_METHOD] == MQTT_DATA_METHOD_SYSINFO_PUBLISHED:
                # If the connected controller publishes sysinfo we expect something to have changed.
                # So ask the list of devices again.
                # To be honest: I don't think this will do anything usefull, as no new entities will be created.
                client.subscribe(self._profile_creation_id + MQTT_TOPIC_SUFFIX_RSP, qos=1)
                client.publish(
                    self._profile_creation_id + MQTT_TOPIC_SUFFIX_CMD,
                    json.dumps({MQTT_DATA_METHOD: MQTT_DATA_METHOD_DEVICES_LIST}),
                    1
                )

            # Device events (/control/devices/evt, method: devices.added)
            elif topic == (self._profile_creation_id + MQTT_TOPIC_SUFFIX_EVT) and \
                    response[MQTT_DATA_METHOD] == MQTT_DATA_METHOD_DEVICES_ADDED:
                if self._process_devices_list(response):
                    self._device_instances['controller'].on_change(topic, response)
                    if self._devices_list_callback:
                        self._devices_list_callback()

            # Device events (/control/devices/evt, method: devices.removed)
            elif topic == (self._profile_creation_id + MQTT_TOPIC_SUFFIX_EVT) and \
                    response[MQTT_DATA_METHOD] == MQTT_DATA_METHOD_DEVICES_REMOVED:
                if self._remove_from_devices_list(response):
                    self._device_instances['controller'].on_change(topic, response)
                    if self._devices_list_callback:
                        self._devices_list_callback()

            # Device events (/control/devices/evt, method: devices.status or devices.changed)
            elif topic == (self._profile_creation_id + MQTT_TOPIC_SUFFIX_EVT) and (
                    response[MQTT_DATA_METHOD] == MQTT_DATA_METHOD_DEVICES_STATUS or
                    response[MQTT_DATA_METHOD] == MQTT_DATA_METHOD_DEVICES_CHANGED
            ):
                self._device_instances['controller'].on_change(topic, response)

                devices = extract_devices(response)

                changes_processed = False
                for device in devices:
                    if MQTT_DATA_PARAMS_DEVICES_UUID not in device:
                        continue

                    try:
                        self._device_instances[device[MQTT_DATA_PARAMS_DEVICES_UUID]].on_change(topic, device)
                        changes_processed = True
                    except KeyError as e:
                        _LOGGER.debug(
                            f'Device not in our instances list, therefor failed to invoke callback: {device[MQTT_DATA_PARAMS_DEVICES_UUID]}. Topic: {topic} | Data: {device}')
                    except Exception as e:
                        _LOGGER.debug(
                            f'Failed to invoke callback: {device[MQTT_DATA_PARAMS_DEVICES_UUID]}. Topic: {topic} | Data: {device}')
                        _LOGGER.exception(e)

                if changes_processed and response[
                    MQTT_DATA_METHOD] == MQTT_DATA_METHOD_DEVICES_CHANGED and self._devices_list_callback:
                    self._devices_list_callback()

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
                    json.dumps({MQTT_DATA_METHOD: MQTT_DATA_METHOD_SYSINFO_PUBLISH}),
                    1
                )

                # ask the devices list
                client.publish(
                    self._profile_creation_id + MQTT_TOPIC_SUFFIX_CMD,
                    json.dumps({MQTT_DATA_METHOD: MQTT_DATA_METHOD_DEVICES_LIST}),
                    1
                )

            elif rc in (1, 2, 3, 4, 5) and on_connection_refused is not None:
                # Possible reasons for Connection refused:
                # 1: Connection refused - incorrect protocol version
                # 2: Connection refused - invalid client identifier
                # 3: Connection refused - server unavailable
                # 4: Connection refused - bad username or password
                # 5: Connection refused - not authorised
                on_connection_refused(rc)
            elif MQTT_RC_CODES[rc]:
                raise Exception(MQTT_RC_CODES[rc])
            else:
                raise Exception('Unknown error')

        def _on_disconnect(client, userdata, rc):
            _LOGGER.warning('Disconnected from MQTT broker')
            for device in self._device_instances.values():
                device.set_disconnected()

        # Configure the callbacks
        self._client.on_message = _on_message
        self._client.on_connect = _on_connect
        self._client.on_disconnect = _on_disconnect

        self._client.connect_async(self._address, self._port)
        self._client.loop_start()

    def disconnect(self):
        self._client.loop_stop()
        self._client.disconnect()

    def get_device_instances(self, device_class):
        return [device for device in self._device_instances.values() if isinstance(device, device_class)]

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
                _LOGGER.debug(f'→ Publishing device control command: {json.dumps(command)}')
                self._client.publish(
                    self._profile_creation_id + MQTT_TOPIC_SUFFIX_CMD,
                    json.dumps(command),
                    1
                )
            sleep(0.05)

    def add_device_control(self, uuid, property_key, property_value):
        while len(self._device_control_buffer.keys()) >= self._device_control_buffer_size or \
                self._device_control_buffer_command_count >= self._device_control_buffer_command_size:
            pass
        sem.acquire()
        self._device_control_buffer_command_count += 1
        if uuid not in self._device_control_buffer:
            self._device_control_buffer[uuid] = {}
        self._device_control_buffer[uuid][property_key] = property_value
        sem.release()

    def _remove_from_devices_list(self, response):
        changes = False
        devices = extract_devices(response)
        for device in devices:
            if device[MQTT_DATA_PARAMS_DEVICES_UUID] in self._device_instances:
                _LOGGER.info(f"Removing device {device[MQTT_DATA_PARAMS_DEVICES_UUID]} from devices list")
                self._device_instances.pop(device[MQTT_DATA_PARAMS_DEVICES_UUID])
                changes = True
        return changes

    def _process_devices_list(self, response):
        """Convert the response of devices.list or devices.added into device instances."""
        _LOGGER.debug(f'Received device list: {response}')
        devices = extract_devices(response)
        changes = False
        for device in devices:
            try:
                # Try to find the class for the device with the technology included
                # This is the most specific class, as for some devices the technology is important.
                # For example the Generic ZigBee Heating/Cooling Implementation is exposed as CocoThermostatHvac, but it
                # should actually be mapped to CocoGenericHvac, as this is a very similar implementation.
                classname = str.replace(
                    str.title(
                        str.replace(
                            'Coco ' + device["Model"] + ' ' + device["Type"] + ' ' + device["Technology"].lower(),
                            '-',
                            ' '
                        )
                    ),
                    ' ',
                    ''
                )

                try:
                    getattr(sys.modules[__name__], classname)
                except AttributeError as e:
                    # Try to find the class for the device, but **without** the technology included
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

                # Ignore some devices. These are devices that:
                # * are not supported by the API / MQTT broker
                # * don't have any (usefull) properties
                if classname in [
                    'CocoAvout010VFanFan',
                    'CocoAvout110VDimmer',
                    'CocoBatterypoweredmotiondetectorMotiondetector',
                    'CocoBatterypushbuttonx1Smartpanel',
                    'CocoBatterypushbuttonx2Smartpanel',
                    'CocoBatterypushbuttonx4Smartpanel',
                    'CocoChimeRelay',
                    'CocoDigitalsensorDigitalsensor',
                    'CocoDimcontrollerSmartpanel',
                    'CocoDimcontrollerfeedbackSmartpanel',
                    'CocoDimcontrollerx2Panel',
                    'CocoDimmerDimmer',
                    'CocoDimmerSmartdimmer',
                    'CocoDoorlockLock',
                    'CocoElectricalheatingHvac',
                    'CocoExtensionbuttonx1Smartextensionpanel',
                    'CocoExternalsystemDigitalsensor',
                    'CocoGasCentralmeter',
                    'CocoGenericAudiocontrol',
                    'CocoGenericBrick',
                    'CocoGenericChargingstation',
                    'CocoGenericGatewayfw',
                    'CocoGenericLightsensor',
                    'CocoGenericRadio',
                    'CocoGenericStick',
                    'CocoHeatingcoolingsystemHvac',
                    'CocoHeatingsystemHvac',
                    'CocoIndoormotiondetectorMotiondetector',
                    'CocoLightRelay',
                    'CocoLightSmartrelay',
                    'CocoMinidetectorMotiondetector',
                    'CocoMoodbuttonPanel',
                    'CocoMotorcontrollerfeedbackPanel',
                    'CocoMotorcontrollerPanel',
                    'CocoMotorcontrollerSmartpanel',
                    'CocoMotorcontrollerx2FeedbackPanel',
                    'CocoMotorcontrollerx2Panel',
                    'CocoNhc2301RTouchswitch',
                    'CocoNhc24Touchswitch',
                    'CocoNhcElectricitymeter',
                    'CocoNhcGasmeter',
                    'CocoOutdoormotiondetectorMotiondetector',
                    'CocoPumpHvac',
                    'CocoPushbuttonx1FeedbackPanel',
                    'CocoPushbuttonx2FeedbackPanel',
                    'CocoPushbuttonx4FeedbackPanel',
                    'CocoPushbuttonx6FeedbackPanel',
                    'CocoPushbuttonx1FeedbackSmartpanel',
                    'CocoPushbuttonx2FeedbackSmartpanel',
                    'CocoPushbuttonx4FeedbackSmartpanel',
                    'CocoPushbuttonx1Panel',
                    'CocoPushbuttonx2Panel',
                    'CocoPushbuttonx4Panel',
                    'CocoPushbuttonx6Panel',
                    'CocoPushbuttonx4Pushbuttoninterface',
                    'CocoPushbuttonx1Smartpanel',
                    'CocoPushbuttonx2Smartpanel',
                    'CocoRolldownshutterMotor',
                    'CocoSocketRelay',
                    'CocoSunblindMotor',
                    'CocoSwitchedFanRelay',
                    'CocoSwitchedGenericRelay',
                    'CocoVdsVds',
                    'CocoVeluxKlf200Motor',
                    'CocoVenetianblindMotor',
                    'CocoVentilationcontrollerfeedbackPanel',
                    'CocoWaterCentralmeter',
                    'CocoZonevalveHvac'
                ]:
                    _LOGGER.debug(f"Skipping {device[MQTT_DATA_PARAMS_DEVICES_UUID]} of {classname}")
                    continue

                instance = getattr(sys.modules[__name__], classname)(json_to_map(device))
                self._device_instances[instance.uuid] = instance
                _LOGGER.debug(f"Added device {instance.uuid} of class {classname}")
                changes = True
            except Exception as e:
                _LOGGER.warning(f"Class {classname} not found: {e}")

        return changes

    def set_devices_list_callback(self, callback):
        self._devices_list_callback = callback

    def set_systeminfo_callback(self, callback):
        self._system_info_callback = callback
