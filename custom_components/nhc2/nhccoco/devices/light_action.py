from .relay_action import CocoRelayAction


class CocoLightAction(CocoRelayAction):
    @property
    def is_on(self) -> bool:
        return self.status_status == 'On'

    @property
    def support_brightness(self) -> bool:
        return False
