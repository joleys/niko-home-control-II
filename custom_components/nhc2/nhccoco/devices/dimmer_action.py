from ..const import PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON, PROPERTY_STATUS_VALUE_OFF, PROPERTY_BRIGHTNESS, \
    PROPERTY_ALIGNED, PROPERTY_ALIGNED_VALUE_TRUE
from ..helpers import to_int_or_none
from .device import CoCoDevice


class CocoDimmerAction(CoCoDevice):
    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def is_status_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_ON

    @property
    def brightness(self) -> int:
        return to_int_or_none(self.extract_property_value(PROPERTY_BRIGHTNESS))

    @property
    def aligned(self) -> str:
        return self.extract_property_value(PROPERTY_ALIGNED)

    @property
    def is_aligned(self) -> bool:
        return self.aligned == PROPERTY_ALIGNED_VALUE_TRUE

    @property
    def support_brightness(self) -> bool:
        return True

    def turn_on(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON)

    def turn_off(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF)

    def set_brightness(self, gateway, brightness: int):
        gateway.add_device_control(self.uuid, PROPERTY_BRIGHTNESS, str(brightness))
