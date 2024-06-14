from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from ..nhccoco.devices.robinsip_videodoorstation import CocoRobinsipVideodoorstation
from .nhc_entity import NHCBaseEntity


class Nhc2RobinsipVideodoorstationStatusEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoRobinsipVideodoorstation, hub, gateway):
        """Initialize a enum sensor."""
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
