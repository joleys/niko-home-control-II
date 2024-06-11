from ..nhccoco.devices.generic_energyhome import CocoGenericEnergyhome
from .nhc_entity import NHCDisableReportInstantUsageReEnablingEntity


class Nhc2GenericEnergyhomeDisableReportInstantUsageReEnablingEntity(NHCDisableReportInstantUsageReEnablingEntity):
    def __init__(self, device_instance: CocoGenericEnergyhome, hub, gateway):
        super().__init__(device_instance, hub, gateway)
