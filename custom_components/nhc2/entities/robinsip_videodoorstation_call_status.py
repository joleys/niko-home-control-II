from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from ..nhccoco.devices.robinsip_videodoorstation import CocoRobinsipVideodoorstation
from .nhc_entity import NHCBaseEntity


class Nhc2RobinsipVideodoorstationCallStatusEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoRobinsipVideodoorstation, hub, gateway, number):
        """Initialize a enum sensor."""
        super().__init__(device_instance, hub, gateway)

        self._number = number

        self._attr_unique_id = f'{device_instance.uuid}_call_status_{self._number:02}'
        self._attr_device_class = SensorDeviceClass.ENUM

    @property
    def name(self) -> str:
        return f'Call status {self._number:02}'

    @property
    def native_value(self):
        method_to_call = f'call_status_{self._number:02}'

        if hasattr(self._device, method_to_call):
            return getattr(self._device, method_to_call)

    @property
    def options(self):
        method_to_call = f'possible_call_statuses_{self._number:02}'

        if hasattr(self._device, method_to_call):
            return getattr(self._device, method_to_call)

    @property
    def state(self) -> str:
        method_to_call = f'call_status_{self._number:02}'

        if hasattr(self._device, method_to_call):
            return getattr(self._device, method_to_call)
