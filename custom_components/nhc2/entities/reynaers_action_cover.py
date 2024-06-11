from homeassistant.components.cover import CoverEntity, CoverDeviceClass, CoverEntityFeature

from ..nhccoco.const import PROPERTY_ACTION_VALUE_OPEN, PROPERTY_ACTION_VALUE_CLOSE, PROPERTY_ACTION_VALUE_STOP, \
    PROPERTY_STATUS_VALUE_FIXED_CLOSED
from ..nhccoco.devices.reynaers_action import CocoReynaersAction
from .nhc_entity import NHCBaseEntity


class Nhc2ReynaersActionCoverEntity(NHCBaseEntity, CoverEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoReynaersAction, hub, gateway):
        """Initialize a cover."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

        self._attr_device_class = CoverDeviceClass.WINDOW
        self._attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP

    @property
    def is_closed(self) -> bool | None:
        return self._device.status == PROPERTY_STATUS_VALUE_FIXED_CLOSED

    async def async_open_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_OPEN)
        self.schedule_update_ha_state()

    async def async_close_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_CLOSE)
        self.schedule_update_ha_state()

    async def async_stop_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_STOP)
        self.schedule_update_ha_state()
