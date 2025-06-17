from ..const import PROPERTY_STATUS, PROPERTY_IP_ADDRESS, PROPERTY_CALL_STATUS_01, PROPERTY_CALL_STATUS_02, \
    PROPERTY_CALL_STATUS_03, PROPERTY_CALL_STATUS_04
from ..helpers import to_float_or_none
from .device import CoCoDevice

import socket
import struct


class CocoRobinsipVideodoorstation(CoCoDevice):
    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def possible_statuses(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_STATUS)

    @property
    def ip_address(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_IP_ADDRESS))

    @property
    def ip_address_readable(self) -> str:
        if self.ip_address is None:
            return None

        return socket.inet_ntoa(struct.pack('!L', int(self.ip_address)))

    @property
    def call_status_01(self) -> str:
        return self.extract_property_value(PROPERTY_CALL_STATUS_01)

    @property
    def possible_call_statuses_01(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_CALL_STATUS_01)

    @property
    def call_status_02(self) -> str:
        return self.extract_property_value(PROPERTY_CALL_STATUS_02)

    @property
    def possible_call_statuses_02(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_CALL_STATUS_02)

    @property
    def supports_call_status_02(self) -> bool:
        return self.has_property(PROPERTY_CALL_STATUS_02)

    @property
    def call_status_03(self) -> str:
        return self.extract_property_value(PROPERTY_CALL_STATUS_03)

    @property
    def possible_call_statuses_03(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_CALL_STATUS_03)

    @property
    def supports_call_status_03(self) -> bool:
        return self.has_property(PROPERTY_CALL_STATUS_03)

    @property
    def call_status_04(self) -> str:
        return self.extract_property_value(PROPERTY_CALL_STATUS_04)

    @property
    def possible_call_statuses_04(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_CALL_STATUS_04)

    @property
    def supports_call_status_04(self) -> bool:
        return self.has_property(PROPERTY_CALL_STATUS_04)
