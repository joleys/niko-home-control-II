from .relay_action import CocoRelayAction


class CocoSwitchedFanAction(CocoRelayAction):
    @property
    def is_on(self) -> bool:
        return self.status_status == 'On'
