from ..nhccoco.devices.generic_smartplug import CocoGenericSmartplug
from .nhc_entity import NHCDisableReportInstantUsageReEnablingEntity


class Nhc2GenericSmartplugDisableReportInstantUsageReEnablingEntity(NHCDisableReportInstantUsageReEnablingEntity):
    def __init__(self, device_instance: CocoGenericSmartplug, hub, gateway):
        super().__init__(device_instance, hub, gateway)
