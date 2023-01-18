from .relay_action import CocoRelayAction


class CocoSwitchedGenericAction(CocoRelayAction):
    @property
    def is_on(self) -> bool:
        return self.status_status == 'On'
