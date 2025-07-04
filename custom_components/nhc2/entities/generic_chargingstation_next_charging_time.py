from datetime import time

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from ..nhccoco.devices.generic_chargingstation import CocoGenericChargingstation
from .nhc_entity import NHCBaseEntity


class Nhc2GenericChargingstationNextChargingTimeEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericChargingstation, hub, gateway):
        """Initialize a time entity."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_next_charging_time'
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_native_value = self._device.next_charging_time

    @property
    def name(self) -> str:
        return 'Next Charging Time'

    @property
    def state(self) -> time:
        return self._device.next_charging_time
