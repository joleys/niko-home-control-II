from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PARAMETER_DECLINE_CALL_APPLIED_ON_ALL_DEVICES, \
    PARAMETER_DECLINE_CALL_APPLIED_ON_ALL_DEVICES_VALUE_TRUE, PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_ON, \
    PROPERTY_BASIC_STATE_VALUE_TRIGGERED, PROPERTY_DOORLOCK, PROPERTY_DOORLOCK_VALUE_OPEN, \
    PROPERTY_DOORLOCK_VALUE_CLOSED, PROPERTY_CALL_PENDING, PROPERTY_CALL_PENDING_VALUE_TRUE, PARAMETER_CALL_ANSWERED, \
    PARAMETER_CALL_ANSWERED_VALUE_TRUE

from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)

import sys
from ...entities.boolean_has_status_true_can_control_false import Nhc2BooleanHasStatusTrueCanControlFalseEntity


class CocoAccesscontrolAction(CoCoDevice):
    @property
    def supports_basicstate(self) -> bool:
        return self.has_property(PROPERTY_BASIC_STATE)

    @property
    def basic_state(self) -> str:
        return self.extract_property_value(PROPERTY_BASIC_STATE)

    @property
    def possible_basic_states(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_BASIC_STATE)

    @property
    def is_basic_state_on(self) -> bool:
        return self.basic_state == PROPERTY_BASIC_STATE_VALUE_ON

    @property
    def supports_doorlock(self) -> bool:
        return self.has_property(PROPERTY_DOORLOCK)

    @property
    def doorlock(self) -> str:
        return self.extract_property_value(PROPERTY_DOORLOCK)

    @property
    def is_doorlock_open(self) -> bool:
        return self.doorlock == PROPERTY_DOORLOCK_VALUE_OPEN

    @property
    def is_doorlock_closed(self) -> bool:
        return self.doorlock == PROPERTY_DOORLOCK_VALUE_CLOSED

    @property
    def call_pending(self) -> bool:
        return self.extract_property_value(PROPERTY_CALL_PENDING) == PROPERTY_CALL_PENDING_VALUE_TRUE

    @property
    def call_answered(self) -> bool:
        return self.extract_parameter_value(PARAMETER_CALL_ANSWERED) == PARAMETER_CALL_ANSWERED_VALUE_TRUE

    @property
    def decline_call_applied_on_all_devices(self) -> bool:
        return self.extract_parameter_value(
            PARAMETER_DECLINE_CALL_APPLIED_ON_ALL_DEVICES
        ) == PARAMETER_DECLINE_CALL_APPLIED_ON_ALL_DEVICES_VALUE_TRUE

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def press(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_TRIGGERED)

    def open_doorlock(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_DOORLOCK, PROPERTY_DOORLOCK_VALUE_OPEN)

    def get_binary_sensor_entities(self, hub: tuple, gateway) -> list:
        entities = []

        for property_definition in self._property_definitions:
            property_name = next(iter(property_definition))
            if property_definition[property_name]['Description'] != 'Boolean':
                continue

            classname = 'Nhc2BooleanHasStatus%sCanControl%sEntity' % (
                'True' if property_definition[property_name]['HasStatus'] == 'true' else 'False',
                'True' if property_definition[property_name]['CanControl'] == 'true' else 'False',
            )

            instance = getattr(sys.modules[__name__], classname)(property_name, self, hub, gateway)
            entities.append(instance)

        if self.has_parameter(PARAMETER_DECLINE_CALL_APPLIED_ON_ALL_DEVICES):
            entities.append(
                Nhc2BooleanHasStatusTrueCanControlFalseEntity(
                    PARAMETER_DECLINE_CALL_APPLIED_ON_ALL_DEVICES, self, hub, gateway, True
                )
            )

        return entities
