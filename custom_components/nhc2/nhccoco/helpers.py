from .const import MQTT_DATA_PARAMS, MQTT_DATA_PARAMS_DEVICES, MQTT_DATA_PARAMS_DEVICES_PROPERTIES, \
    MQTT_DATA_PARAMS_DEVICES_UUID, MQTT_DATA_METHOD, MQTT_DATA_METHOD_DEVICES_CONTROL, MQTT_DATA_PARAMS_SYSTEMINFO, \
    MQTT_DATA_PARAMS_SYSTEMINFO_SWVERSIONS, MQTT_DATA_PARAMS_SYSTEMINFO_SWVERSIONS_COCO_IMAGE, \
    MQTT_DATA_PARAMS_SYSTEMINFO_SWVERSIONS_NHC_VERSION


def extract_versions(nhc2_sysinfo):
    """Return the versions, extracted from sysinfo."""
    params = nhc2_sysinfo[MQTT_DATA_PARAMS]
    system_info = next(
        filter(
            (lambda x: x and MQTT_DATA_PARAMS_SYSTEMINFO in x),
            params
        ), None
    )[MQTT_DATA_PARAMS_SYSTEMINFO]

    s_w_versions = next(
        filter(
            (lambda x: x and MQTT_DATA_PARAMS_SYSTEMINFO_SWVERSIONS in x),
            system_info
        ), None
    )[MQTT_DATA_PARAMS_SYSTEMINFO_SWVERSIONS]

    coco_image = next(
        filter(
            (lambda x: x and MQTT_DATA_PARAMS_SYSTEMINFO_SWVERSIONS_COCO_IMAGE in x),
            s_w_versions
        ), None
    )[MQTT_DATA_PARAMS_SYSTEMINFO_SWVERSIONS_COCO_IMAGE]

    nhc_version = next(
        filter(
            (lambda x: x and MQTT_DATA_PARAMS_SYSTEMINFO_SWVERSIONS_NHC_VERSION in x),
            s_w_versions
        ), None
    )[MQTT_DATA_PARAMS_SYSTEMINFO_SWVERSIONS_NHC_VERSION]

    return coco_image, nhc_version


def extract_devices(response):
    params = response[MQTT_DATA_PARAMS]
    param_with_devices = next(filter((lambda x: x and MQTT_DATA_PARAMS_DEVICES in x), params), None)
    return param_with_devices[MQTT_DATA_PARAMS_DEVICES]


def process_device_commands(device_commands_to_process):
    devices = []
    for uuid, properties in device_commands_to_process.items():
        device = {MQTT_DATA_PARAMS_DEVICES_UUID: uuid, MQTT_DATA_PARAMS_DEVICES_PROPERTIES: []}
        for property_key, property_value in properties.items():
            device[MQTT_DATA_PARAMS_DEVICES_PROPERTIES].append({property_key: property_value})
        devices.append(device)
    return {
        MQTT_DATA_METHOD: MQTT_DATA_METHOD_DEVICES_CONTROL,
        MQTT_DATA_PARAMS: [{
            MQTT_DATA_PARAMS_DEVICES: devices
        }]
    }


def json_to_map(json):
    return {k: v for k, v in json.items()}


def to_float_or_none(value) -> float | None:
    if value is None or value == '':
        return None
    return float(value)


def to_int_or_none(value) -> int | None:
    if value is None or value == '':
        return None
    return int(float(value))
