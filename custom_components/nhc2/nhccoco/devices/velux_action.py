from ..const import PROPERTY_ACTION, PROPERTY_FEEDBACK
from .device import CoCoDevice


class CocoVeluxAction(CoCoDevice):
    @property
    def action(self) -> str:
        return self.extract_property_value(PROPERTY_ACTION)

    @property
    def feedback(self) -> str:
        return self.extract_property_value(PROPERTY_FEEDBACK)

    @property
    def possible_feedback(self) -> list:
        return self.extract_property_definition_description_choices(PROPERTY_FEEDBACK)

    @property
    def supports_feedback(self) -> bool:
        return self.has_property(PROPERTY_FEEDBACK)

    def set_action(self, gateway, action: str):
        gateway.add_device_control(self.uuid, PROPERTY_ACTION, action)
