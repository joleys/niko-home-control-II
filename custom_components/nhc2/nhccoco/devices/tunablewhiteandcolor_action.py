from ..const import PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON, PROPERTY_STATUS_VALUE_OFF, PROPERTY_BRIGHTNESS, \
    PROPERTY_BRIGHTNESS_ALIGNED, PROPERTY_BRIGHTNESS_ALIGNED_VALUE_TRUE, PROPERTY_COLOR_ALIGNED, \
    PROPERTY_COLOR_ALIGNED_VALUE_TRUE
from ..helpers import to_int_or_none
from .device import CoCoDevice


class CocoTunablewhiteandcolorAction(CoCoDevice):
    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def is_status_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_ON

    def turn_on(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON)

    def turn_off(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF)

    @property
    def brightness(self) -> int:
        return to_int_or_none(self.extract_property_value(PROPERTY_BRIGHTNESS))

    @property
    def brightness_aligned(self) -> str:
        return self.extract_property_value(PROPERTY_BRIGHTNESS_ALIGNED)

    @property
    def is_brightness_aligned(self) -> bool:
        return self.brightness_aligned == PROPERTY_BRIGHTNESS_ALIGNED_VALUE_TRUE

    @property
    def support_brightness(self) -> bool:
        return True

    @property
    def color_aligned(self) -> str:
        return self.extract_property_value(PROPERTY_COLOR_ALIGNED)

    @property
    def is_color_aligned(self) -> bool:
        return self.color_aligned == PROPERTY_COLOR_ALIGNED_VALUE_TRUE

    def set_brightness(self, gateway, brightness: int):
        gateway.add_device_control(self.uuid, PROPERTY_BRIGHTNESS, str(brightness))
