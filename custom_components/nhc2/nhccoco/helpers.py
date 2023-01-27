from .const import KEY_DEVICES, KEY_PARAMS, KEY_PROPERTIES, KEY_UUID, KEY_METHOD, MQTT_METHOD_DEVICES_CONTROL

import logging

_LOGGER = logging.getLogger(__name__)


def extract_devices(response):
    params = response[KEY_PARAMS]
    param_with_devices = next(filter((lambda x: x and KEY_DEVICES in x), params), None)
    return param_with_devices[KEY_DEVICES]


def extract_property_value_from_device(device, property_key):
    if device and KEY_PROPERTIES in device:
        properties = device[KEY_PROPERTIES]
        if properties:
            property_object = next(filter((lambda x: x and property_key in x), properties), None)
            if property_object and property_key in property_object:
                return property_object[property_key]
    return None


def extract_property_definitions(response, parameter):
    if response and 'PropertyDefinitions' in response:
        properties = response['PropertyDefinitions']
        if properties:
            return next(filter((lambda x: x and parameter in x), properties), None)[parameter]
    else:
        return None


def dev_prop_changed(field, dev, prop):
    return prop in dev and field != dev[prop]


def process_device_commands(device_commands_to_process):
    devices = []
    for uuid, properties in device_commands_to_process.items():
        device = {KEY_UUID: uuid, KEY_PROPERTIES: []}
        for property_key, property_value in properties.items():
            device[KEY_PROPERTIES].append({property_key: property_value})
        devices.append(device)
    return {
        KEY_METHOD: MQTT_METHOD_DEVICES_CONTROL,
        KEY_PARAMS: [{
            KEY_DEVICES: devices
        }]
    }


def json_to_map(json):
    return {k: v for k, v in json.items()}


def to_float_or_none(value) -> float | None:
    if value is None or value == '':
        return None
    return float(value)
def to_int_or_none(value) -> float | None:
    if value is None or value == '':
        return None
    return int(value)
