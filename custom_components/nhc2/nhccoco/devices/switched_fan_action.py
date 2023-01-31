from ..const import PROPERTY_STATUS_VALUE_ON
from .relay_action import CocoRelayAction


class CocoSwitchedFanAction(CocoRelayAction):
    @property
    def is_status_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_ON
