from homeassistant.components.button import ButtonEntity

from ..nhccoco.devices.comfort_action import CocoComfortAction
from .nhc_entity import NHCBaseEntity


class Nhc2ComfortActionButtonEntity(NHCBaseEntity, ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoComfortAction, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

    @property
    def is_on(self) -> bool:
        return self._device.is_basic_state_on

    async def async_press(self) -> None:
        self._device.press(self._gateway)
        self.schedule_update_ha_state()
