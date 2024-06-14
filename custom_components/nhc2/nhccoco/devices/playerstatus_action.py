from ..const import PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_ON, PROPERTY_FEEDBACK_MESSAGE
from .device import CoCoDevice


class CocoPlayerstatusAction(CoCoDevice):
    @property
    def basic_state(self) -> str:
        return self.extract_property_value(PROPERTY_BASIC_STATE)

    @property
    def is_basic_state_on(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_ON

    @property
    def feedback_message(self) -> str:
        return self.extract_property_value(PROPERTY_FEEDBACK_MESSAGE)
