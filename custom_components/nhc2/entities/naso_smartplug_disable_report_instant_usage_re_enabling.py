from ..nhccoco.devices.naso_smartplug import CocoNasoSmartplug
from .nhc_entity import NHCDisableReportInstantUsageReEnablingEntity


class Nhc2NasoSmartplugDisableReportInstantUsageReEnablingEntity(NHCDisableReportInstantUsageReEnablingEntity):
    def __init__(self, device_instance: CocoNasoSmartplug, hub, gateway):
        super().__init__(device_instance, hub, gateway)
