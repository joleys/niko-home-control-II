from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from ..nhccoco.devices.bellbutton_action import CocoBellbuttonAction
from .nhc_entity import NHCBaseEntity


class Nhc2BellbuttonActionBasicStateEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoBellbuttonAction, hub, gateway):
        """Initialize a enum sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_basic_state'

        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = self._device.possible_basic_states
        self._attr_native_value = self._device.basic_state

    @property
    def name(self) -> str:
        return 'Basic State'

    @property
    def state(self) -> str:
        return self._device.basic_state
