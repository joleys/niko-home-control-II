from ..const import PROPERTY_ACTION, PROPERTY_STATUS
from .device import CoCoDevice


class CocoReynaersAction(CoCoDevice):
    @property
    def action(self) -> str:
        return self.extract_property_value(PROPERTY_ACTION)

    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def possible_statuses(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_STATUS)

    def set_action(self, gateway, action: str):
        gateway.add_device_control(self.uuid, PROPERTY_ACTION, action)
