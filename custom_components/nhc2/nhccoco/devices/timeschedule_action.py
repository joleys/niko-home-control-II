from ..const import PROPERTY_ACTIVE, PROPERTY_ACTIVE_VALUE_TRUE
from .device import CoCoDevice


class CocoTimescheduleAction(CoCoDevice):
    @property
    def active(self) -> str:
        return self.extract_property_value(PROPERTY_ACTIVE)

    @property
    def is_active(self) -> bool:
        return self.active == PROPERTY_ACTIVE_VALUE_TRUE
