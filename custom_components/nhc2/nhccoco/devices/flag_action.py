from ..const import PROPERTY_STATUS, PROPERTY_STATUS_VALUE_TRUE, PROPERTY_STATUS_VALUE_FALSE
from .device import CoCoDevice


class CocoFlagAction(CoCoDevice):
    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def is_status_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_TRUE

    def turn_on(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_TRUE)

    def turn_off(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_FALSE)
