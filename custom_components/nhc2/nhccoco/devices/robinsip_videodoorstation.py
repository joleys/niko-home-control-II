from ..const import PROPERTY_STATUS, PROPERTY_IP_ADDRESS, PROPERTY_CALL_STATUS_01
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
