from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from ..nhccoco.devices.robinsip_videodoorstation import CocoRobinsipVideodoorstation
from .nhc_entity import NHCBaseEntity


class Nhc2RobinsipVideodoorstationCallStatus01Entity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoRobinsipVideodoorstation, hub, gateway):
        """Initialize a enum sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_call_status_01'

        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = self._device.possible_call_statuses_01
        self._attr_native_value = self._device.call_status_01

    @property
    def name(self) -> str:
        return 'Call Status 01'

    @property
    def state(self) -> str:
        return self._device.call_status_01
