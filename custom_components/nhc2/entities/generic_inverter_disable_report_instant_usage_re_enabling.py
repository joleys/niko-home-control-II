from ..nhccoco.devices.generic_inverter import CocoGenericInverter
from .nhc_entity import NHCDisableReportInstantUsageReEnablingEntity


class Nhc2GenericInverterDisableReportInstantUsageReEnablingEntity(NHCDisableReportInstantUsageReEnablingEntity):
    def __init__(self, device_instance: CocoGenericInverter, hub, gateway):
        super().__init__(device_instance, hub, gateway)
