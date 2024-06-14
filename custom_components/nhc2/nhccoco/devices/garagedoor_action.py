from ..const import PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_OFF, PROPERTY_BASIC_STATE_VALUE_ON, \
    PROPERTY_BASIC_STATE_VALUE_INTERMEDIATE, PROPERTY_BASIC_STATE_VALUE_TRIGGERED, PROPERTY_PORT_CLOSED, \
    PROPERTY_PORT_CLOSED_VALUE_TRUE, GARAGE_DOOR_STATUS_OPENING, GARAGE_DOOR_STATUS_CLOSING
from .device import CoCoDevice


class CocoGaragedoorAction(CoCoDevice):
    def __init__(self, json: dict):
        super().__init__(json)
        self._previous_state = None

    @property
    def basic_state(self) -> str:
        return self.extract_property_value(PROPERTY_BASIC_STATE)

    @property
    def possible_basic_states(self) -> list:
        states = self.extract_property_definition_description_choices(PROPERTY_BASIC_STATE)
        states.remove(PROPERTY_BASIC_STATE_VALUE_TRIGGERED)

        return states

    @property
    def is_basic_state_on(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_ON

    @property
    def is_basic_state_off(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_OFF

    @property
    def is_basic_state_intermediate(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_INTERMEDIATE

    @property
    def port_closed(self) -> str:
        return self.extract_property_value(PROPERTY_PORT_CLOSED)

    @property
    def is_port_closed(self) -> bool:
        return self.port_closed == PROPERTY_PORT_CLOSED_VALUE_TRUE

    @property
    def is_port_open(self) -> bool:
        return self.port_closed != PROPERTY_PORT_CLOSED_VALUE_TRUE

    @property
    def supports_port_closed(self) -> bool:
        return self.has_property(PROPERTY_PORT_CLOSED)

    @property
    def current_status(self) -> str | None:
        if self.is_basic_state_intermediate and self._previous_state == PROPERTY_BASIC_STATE_VALUE_OFF:
            return GARAGE_DOOR_STATUS_OPENING
        if self.is_basic_state_intermediate and self._previous_state == PROPERTY_BASIC_STATE_VALUE_ON:
            return GARAGE_DOOR_STATUS_CLOSING
        return None

    @property
    def is_closing(self) -> bool | None:
        return self.current_status == GARAGE_DOOR_STATUS_CLOSING

    @property
    def is_opening(self) -> bool | None:
        return self.current_status == GARAGE_DOOR_STATUS_OPENING

    def on_change(self, topic: str, payload: dict):
        self._previous_state = self.basic_state
        super.on_change(topic, payload)

    def trigger(self, gateway):
        gateway.add_device_control(
            self.uuid,
            PROPERTY_BASIC_STATE,
            PROPERTY_BASIC_STATE_VALUE_TRIGGERED
        )
