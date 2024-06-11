from ..nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .nhc_entity import NHCDisableReportInstantUsageReEnablingEntity


class Nhc2ElectricityClampCentralmeterDisableReportInstantUsageReEnablingEntity(
    NHCDisableReportInstantUsageReEnablingEntity):
    def __init__(self, device_instance: CocoElectricityClampCentralmeter, hub, gateway):
        super().__init__(device_instance, hub, gateway)
