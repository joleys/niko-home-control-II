from ..const import PROPERTY_FAN_SPEED
from .device import CoCoDevice


class CocoFanAction(CoCoDevice):
    @property
    def fan_speed(self) -> str:
        return self.extract_property_value(PROPERTY_FAN_SPEED)

    @property
    def possible_fan_speeds(self) -> list[str]:
        return self.extract_property_definition_description_choices(PROPERTY_FAN_SPEED)

    def set_fan_speed(self, gateway, speed: str):
        gateway.add_device_control(
            self.uuid,
            PROPERTY_FAN_SPEED,
            speed
        )
