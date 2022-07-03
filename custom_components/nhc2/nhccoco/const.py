import paho.mqtt.client as mqtt

from enum import Enum

MQTT_TLS_VERSION = 2
MQTT_PROTOCOL = mqtt.MQTTv311
MQTT_TRANSPORT = "tcp"
MQTT_CERT_FILE = '/coco_ca.pem'

VALUE_DIMMER = 'dimmer'

LIST_VALID_LIGHTS = ['light', VALUE_DIMMER]
LIST_VALID_SWITCHES = ['socket', 'switched-generic']
LIST_VALID_COVERS = ['rolldownshutter', 'sunblind', 'gate', 'venetianblind', 'garagedoor']
LIST_VALID_FANS = ['fan']
LIST_VALID_SWITCHED_FANS = ['switched-fan']
LIST_VALID_THERMOSTATS = ['thermostat']
LIST_VALID_ENERGYMETERS = ['electricity-clamp']
LIST_VALID_ACCESSCONTROL = ['accesscontrol']
LIST_VALID_GENERICS = ['generic']

DEVICE_CONTROL_BUFFER_SIZE = 16
DEVICE_CONTROL_BUFFER_COMMAND_SIZE = 32

KEY_ACTION = 'Action'
KEY_BRIGHTNESS = 'Brightness'
KEY_DEVICES = 'Devices'
KEY_DISPLAY_NAME = 'DisplayName'
KEY_ENTITY = 'entity'
KEY_FAN_SPEED = 'FanSpeed'
KEY_METHOD = 'Method'
KEY_MODEL = 'Model'
KEY_NAME = 'Name'
KEY_ONLINE = 'Online'
KEY_PARAMS = 'Params'
KEY_PROPERTIES = 'Properties'
KEY_POSITION = 'Position'
KEY_STATUS = 'Status'
KEY_TYPE = 'Type'
KEY_UUID = 'Uuid'
KEY_BASICSTATE = "BasicState"

VALUE_ON = 'On'
VALUE_OFF = 'Off'
VALUE_OPEN = 'Open'
VALUE_STOP = 'Stop'
VALUE_CLOSE = 'Close'
VALUE_TRIGGERED = 'Triggered'

GATE_VALUE_OPEN = 'On'
GATE_VALUE_CLOSE = 'Off'
GATE_VALUE_TRIGGERED = 'Triggered'
GATE_MOVING = 'Intermediate'
KEY_ALIGNED = "Aligned"

THERM_PROGRAM = 'Program'
THERM_OVERRULEACTION = 'OverruleActive'
THERM_OVERRULESETPOINT = 'OverruleSetpoint'
THERM_OVERRULETIME = 'OverruleTime'
THERM_ECOSAVE = 'EcoSave'

ENERGY_REPORT = 'ReportInstantUsage'
ENERGY_POWER = 'ElectricalPower'

DEV_TYPE_ACTION = 'action'

INTERNAL_KEY_CALLBACK = 'callbackHolder'
INTERNAL_KEY_MODELS = 'models'
INTERNAL_KEY_CLASS = 'class'

CALLBACK_HOLDER_PROP = 'callbackHolder'

MQTT_METHOD_SYSINFO_PUBLISH = 'systeminfo.publish'
MQTT_METHOD_SYSINFO_PUBLISHED = 'systeminfo.published'
MQTT_METHOD_DEVICES_LIST = 'devices.list'
MQTT_METHOD_DEVICES_CONTROL = 'devices.control'
MQTT_METHOD_DEVICES_STATUS = 'devices.status'
MQTT_METHOD_DEVICES_CHANGED = 'devices.changed'

MQTT_RC_CODES = ['',
                 'Connection refused - incorrect protocol version',
                 'Connection refused - invalid client identifier',
                 'Connection refused - server unavailable',
                 'Connection refused - bad username or password',
                 'Connection refused - not authorised']

MQTT_TOPIC_PUBLIC_AUTH_CMD = 'public/authentication/cmd'
MQTT_TOPIC_PUBLIC_AUTH_RSP = 'public/authentication/rsp'
MQTT_TOPIC_SUFFIX_SYS_EVT = '/system/evt'
MQTT_TOPIC_PUBLIC_CMD = '/system/cmd'
MQTT_TOPIC_PUBLIC_RSP = '/system/rsp'
MQTT_TOPIC_SUFFIX_CMD = '/control/devices/cmd'
MQTT_TOPIC_SUFFIX_RSP = '/control/devices/rsp'
MQTT_TOPIC_SUFFIX_EVT = '/control/devices/evt'