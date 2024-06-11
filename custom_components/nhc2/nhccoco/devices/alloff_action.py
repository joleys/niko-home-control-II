from ..const import PROPERTY_BASIC_STATE, PROPERTY_ALL_OFF_ACTIVE, \
    PROPERTY_ALL_OFF_ACTIVE_VALUE_TRUE, PROPERTY_BASIC_STATE_VALUE_ON, PROPERTY_BASIC_STATE_VALUE_TRIGGERED, \
    PROPERTY_ALL_STARTED, PROPERTY_ALL_STARTED_VALUE_TRUE
from .device import CoCoDevice


class CocoAlloffAction(CoCoDevice):
    @property
    def basic_state(self) -> str:
        return self.extract_property_value(PROPERTY_BASIC_STATE)

    @property
    def is_basic_state_on(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_ON

    @property
    def all_off_active(self) -> str:
        return self.extract_property_value(PROPERTY_ALL_OFF_ACTIVE)

    @property
    def is_all_off_active(self) -> bool:
        return self.all_off_active == PROPERTY_ALL_OFF_ACTIVE_VALUE_TRUE

    @property
    def all_started(self) -> str:
        return self.extract_property_value(PROPERTY_ALL_STARTED)

    @property
    def is_all_started(self) -> bool:
        return self.all_started == PROPERTY_ALL_STARTED_VALUE_TRUE

    @property
    def supports_all_started(self) -> bool:
        return self.has_property(PROPERTY_ALL_STARTED)

    def press(self, gateway):
        gateway.add_device_control(
            self.uuid,
            PROPERTY_BASIC_STATE,
            PROPERTY_BASIC_STATE_VALUE_TRIGGERED
        )
