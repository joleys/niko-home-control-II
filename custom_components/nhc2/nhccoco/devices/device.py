import logging

_LOGGER = logging.getLogger(__name__)


class CoCoDevice():
    def __init__(self, json: dict):
        self._uuid = json['Uuid']
        self._type = json['Type']
        self._technology = json['Technology']
        self._model = json['Model']
        self._identifier = json['Identifier']
        self._name = json['Name']
        self._traits = json['Traits'] if 'Traits' in json else None
        self._parameters = json['Parameters'] if 'Parameters' in json else None
        self._properties = json['Properties'] if 'Properties' in json else None

        self._after_change_callbacks = []
        self._online = json['Online'] if 'Online' in json else None

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
        return self._online == 'True'

    @property
    def after_change_callbacks(self):
        return self._after_change_callbacks

    def extract_parameter_value(self, parameter_key: str) -> str:
        if self._parameters:
            parameter_object = next(filter((lambda x: x and parameter_key in x), self._parameters), None)
            if parameter_object and parameter_key in parameter_object:
                return parameter_object[parameter_key]
        return None

    def extract_property_value(self, property_key: str) -> str:
        if self._properties:
            property_object = next(filter((lambda x: x and property_key in x), self._properties), None)
            if property_object and property_key in property_object:
                return property_object[property_key]
        return None

    def merge_properties(self, new_properties: dict):
        """Merge the properties of the device with the properties of the payload"""
        for new_property in new_properties:
            for key, new_value in new_property.items():
                for index, current_property in enumerate(self._properties):
                    for current_key, current_value in current_property.items():
                        if current_key == key:
                            self._properties[index] = new_property

    def on_change(self, topic: str, payload: dict):
        """Fallback on change method"""
        _LOGGER.debug(f'{self._name} has not implemented the on_change method')
