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
        self._traits = json[DEVICE_DESCRIPTOR_TRAITS] if DEVICE_DESCRIPTOR_TRAITS in json else None
        self._parameters = json[DEVICE_DESCRIPTOR_PARAMETERS] if DEVICE_DESCRIPTOR_PARAMETERS in json else None
        self._properties = json[DEVICE_DESCRIPTOR_PROPERTIES] if DEVICE_DESCRIPTOR_PROPERTIES in json else None
        self._property_definitions = None
        if DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS in json:
            self._property_definitions = json[DEVICE_DESCRIPTOR_PROPERTY_DEFINITIONS]

        self._after_change_callbacks = []
        self._online = json[DEVICE_DESCRIPTOR_ONLINE] if DEVICE_DESCRIPTOR_ONLINE in json else None

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
        if self._online is None:
            return None
        return self._online == DEVICE_DESCRIPTOR_ONLINE_VALUE_TRUE

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
        if self._parameters:
            parameter_object = next(filter((lambda x: x and parameter_key in x), self._parameters), None)
            if parameter_object and parameter_key in parameter_object:
                return parameter_object[parameter_key]
        return None

    def has_parameter(self, parameter_key: str) -> bool:
        if self._parameters:
            parameter_object = next(filter((lambda x: x and parameter_key in x), self._parameters), None)
            if parameter_object and parameter_key in parameter_object:
                return True
        return False

    def extract_property_value(self, property_key: str) -> str:
        if self._properties:
            property_object = next(filter((lambda x: x and property_key in x), self._properties), None)
            if property_object and property_key in property_object:
                return property_object[property_key]
        return None

    def has_property(self, property_key: str) -> bool:
        if self._properties:
            property_object = next(filter((lambda x: x and property_key in x), self._properties), None)
            if property_object and property_key in property_object:
                return True
        return False

    def merge_properties(self, new_properties: dict):
        """Merge the properties of the device with the properties of the payload"""
        for new_property in new_properties:
            for key, new_value in new_property.items():
                for index, current_property in enumerate(self._properties):
                    for current_key, current_value in current_property.items():
                        if current_key == key:
                            self._properties[index] = new_property

    def extract_property_definition(self, property_key: str) -> str:
        if self._property_definitions:
            property_definition_object = next(filter((lambda x: x and property_key in x), self._property_definitions),
                                              None)
            if property_definition_object and property_key in property_definition_object:
                return property_definition_object[property_key]
        return None

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
        """Fallback on change method"""
        _LOGGER.debug(f'{self._name} has not implemented the on_change method')

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
