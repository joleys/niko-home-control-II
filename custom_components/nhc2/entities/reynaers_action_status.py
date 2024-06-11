from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from ..nhccoco.devices.reynaers_action import CocoReynaersAction
from .nhc_entity import NHCBaseEntity


class Nhc2ReynaersActionStatusEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoReynaersAction, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_status'

        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = self._device.possible_statuses
        self._attr_native_value = self._device.status

    @property
    def name(self) -> str:
        return 'Status'

    @property
    def state(self) -> str:
        return self._device.status
