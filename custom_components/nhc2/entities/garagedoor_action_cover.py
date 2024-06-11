from homeassistant.components.cover import CoverEntity, CoverDeviceClass, CoverEntityFeature, ATTR_POSITION

from ..nhccoco.devices.garagedoor_action import CocoGaragedoorAction
from .nhc_entity import NHCBaseEntity


class Nhc2GaragedoorActionCoverEntity(NHCBaseEntity, CoverEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoGaragedoorAction, hub, gateway):
        """Initialize a light."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

        self._attr_device_class = CoverDeviceClass.GARAGE
        self._attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    @property
    def is_closed(self) -> bool:
        if self._device.supports_port_closed:
            return self._device.is_port_closed

        return self._device.is_basic_state_off

    @property
    def is_opening(self) -> bool | None:
        return self._device.is_opening

    @property
    def is_closing(self) -> bool | None:
        return self._device.is_closing

    async def async_open_cover(self):
        self._device.trigger(self._gateway)
        self.schedule_update_ha_state()

    async def async_close_cover(self):
        self._device.trigger(self._gateway)
        self.schedule_update_ha_state()
