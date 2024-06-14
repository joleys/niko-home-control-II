from homeassistant.components.button import ButtonEntity

from ..nhccoco.devices.electricalheating_action import CocoElectricalheatingAction
from .nhc_entity import NHCBaseEntity


class Nhc2ElectricalHeatingActionButtonEntity(NHCBaseEntity, ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoElectricalheatingAction, hub, gateway):
        """Initialize a button."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

    @property
    def is_on(self) -> bool:
        return self._device.is_basic_state_on

    async def async_press(self) -> None:
        self._device.press(self._gateway)
        self.schedule_update_ha_state()
