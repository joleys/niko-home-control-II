from ..const import DEVICE_DESCRIPTOR_UUID, DEVICE_DESCRIPTOR_TYPE, DEVICE_DESCRIPTOR_TECHNOLOGY, \
    DEVICE_DESCRIPTOR_MODEL, DEVICE_DESCRIPTOR_IDENTIFIER, DEVICE_DESCRIPTOR_NAME, DEVICE_DESCRIPTOR_TRAITS, \
    DEVICE_DESCRIPTOR_PARAMETERS, DEVICE_DESCRIPTOR_PROPERTIES, DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS, \
    DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS_DESCRIPTION, DEVICE_DESCRIPTOR_ONLINE, DEVICE_DESCRIPTOR_ONLINE_VALUE_TRUE, \
    DEVICE_DESCRIPTOR_TECHNOLOGY_NIKOHOMECONTROL, PARAMETER_LOCATION_NAME, PARAMETER_MANUFACTURER
from ...const import DOMAIN, BRAND
from typing import Union
import re
import logging

_LOGGER = logging.getLogger(__name__)


class CoCoDevice():
    def __init__(self, json: dict):
        self._uuid = json[DEVICE_DESCRIPTOR_UUID]
        self._type = json[DEVICE_DESCRIPTOR_TYPE]
        self._technology = json[DEVICE_DESCRIPTOR_TECHNOLOGY]
        self._model = json[DEVICE_DESCRIPTOR_MODEL]
        self._identifier = json[DEVICE_DESCRIPTOR_IDENTIFIER]
        self._name = json[DEVICE_DESCRIPTOR_NAME]

        self._property_definitions = {}
        if DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS in json:
            self.obj_arr_to_dict(json[DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS], self._property_definitions)

        self._parameters = {}
        if DEVICE_DESCRIPTOR_PARAMETERS in json:
            self.obj_arr_to_dict(json[DEVICE_DESCRIPTOR_PARAMETERS], self._parameters)

        self._properties = {}
        if DEVICE_DESCRIPTOR_PROPERTIES in json:
            self.obj_arr_to_dict(json[DEVICE_DESCRIPTOR_PROPERTIES], self._properties)

        self._traits = {}
        if DEVICE_DESCRIPTOR_TRAITS in json:
            self.obj_arr_to_dict(json[DEVICE_DESCRIPTOR_TRAITS], self._traits)

        self._after_change_callbacks = []

        # When a device is added we don't always have the latest online state yet so better assume it's online by default
        self._online = json[DEVICE_DESCRIPTOR_ONLINE] == DEVICE_DESCRIPTOR_ONLINE_VALUE_TRUE if DEVICE_DESCRIPTOR_ONLINE in json else True
        if not self._online:
            _LOGGER.debug(f"Device {self._uuid} is offline")

    @property
    def uuid(self) -> str:
        """Unique Identifier within the Niko Home Control Platform, used for addressing the device"""
        return self._uuid

    @property
    def type(self) -> str:
        """Device application type"""
        return self._type

    @property
    def technology(self) -> str:
        """Defines the manufacturer of the device"""
        return self._technology

    @property
    def model(self) -> str:
        """Defines the hardware model"""
        return self._model

    @property
    def identifier(self) -> str:
        """Niko Home Control configuration identifier"""
        return self._identifier

    @property
    def name(self) -> str:
        """Human-readable, display name of the device, can be updated by the user installer"""
        return self._name

    @property
    def parameters(self) -> dict:
        """List of device configuration options"""
        return self._parameters

    @property
    def properties(self) -> dict:
        """List of run-time functions"""
        return self._properties

    @property
    def is_online(self) -> bool:
        """Device is online"""
        return self._online

    @property
    def suggested_area(self) -> str:
        """Suggested area for the device"""
        if self.has_parameter(PARAMETER_LOCATION_NAME):
            return self.extract_parameter_value(PARAMETER_LOCATION_NAME)

        return None

    @property
    def manufacturer(self) -> str:
        if self.has_parameter(PARAMETER_MANUFACTURER):
            return self.extract_parameter_value(PARAMETER_MANUFACTURER)

        return None

    @property
    def after_change_callbacks(self):
        return self._after_change_callbacks

    def extract_parameter_value(self, parameter_key: str) -> str:
        return self._parameters.get(parameter_key, "")

    def has_parameter(self, parameter_key: str) -> bool:
        return parameter_key in self._parameters

    def extract_property_value(self, property_key: str) -> str:
        return self._properties.get(property_key, "")

    def has_property(self, property_key: str) -> bool:
        return property_key in self._properties

    def obj_arr_to_dict(self, obj_arr_in: dict, dict_out: dict):
        for obj in obj_arr_in:
            for k, v in obj.items():
                dict_out[k] = v

    def extract_property_definition(self, property_key: str) -> str | None:
        return self._property_definitions.get(property_key, None)

    def extract_property_definition_description_choices(self, property_key: str) -> Union[list, None]:
        definition = self.extract_property_definition(property_key)
        if definition and DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS_DESCRIPTION in definition:
            choices = re.findall(r'Choice\((.*?)\)', definition[DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS_DESCRIPTION])
            if len(choices) == 1:
                return choices[0].split(',')

        return None

    def extract_property_definition_description_range(self, property_key: str):
        definition = self.extract_property_definition(property_key)
        if definition and DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS_DESCRIPTION in definition:
            range = re.findall(r'Range\((.*?)\)', definition[DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS_DESCRIPTION])
            if len(range) == 1:
                options = range[0].split(',')

                if len(options) == 3:
                    return [
                        float(options[0]),
                        float(options[1]),
                        float(options[2]),
                    ]

        return None

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.obj_arr_to_dict(payload[DEVICE_DESCRIPTOR_PROPERTIES], self._properties)

        if DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS in payload and len(payload[DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS]):
            self.obj_arr_to_dict(payload[DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS], self._property_definitions)

        if DEVICE_DESCRIPTOR_ONLINE in payload:
            self._online = payload[DEVICE_DESCRIPTOR_ONLINE] == DEVICE_DESCRIPTOR_ONLINE_VALUE_TRUE

        for callback in self._after_change_callbacks:
            callback()

    def set_disconnected(self):
        self._online = False

    def device_info(self, hub: str):
        """Return the device info."""

        manufacturer = BRAND
        if self.manufacturer:
            manufacturer += f' ({self.manufacturer})'
        elif self.technology and self.technology != DEVICE_DESCRIPTOR_TECHNOLOGY_NIKOHOMECONTROL:
            manufacturer += f' ({self.technology})'

        return {
            'identifiers': {
                (DOMAIN, self.uuid)
            },
            'name': self.name,
            'manufacturer': manufacturer,
            'model': str.title(f'{self.model} ({self.type})'),
            'via_device': hub,
            'suggested_area': self.suggested_area,
        }
