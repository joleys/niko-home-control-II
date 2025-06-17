from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .nhc_entity import NHCBaseEntity


class Nhc2ElectricityClampCentralmeterInverterTypeEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoElectricityClampCentralmeter, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_inverter_type'

        self._attr_native_value = self._device.inverter_type
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Inverter Type'

    @property
    def state(self) -> str:
        return self._device.inverter_type
