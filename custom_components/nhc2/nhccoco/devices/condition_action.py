from ..const import PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_ON, PROPERTY_BASIC_STATE_VALUE_TRIGGERED
from .device import CoCoDevice


class CocoConditionAction(CoCoDevice):
    @property
    def basic_state(self) -> str:
        return self.extract_property_value(PROPERTY_BASIC_STATE)

    @property
    def is_basic_state_on(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_ON

    def press(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_TRIGGERED)
