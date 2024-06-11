from homeassistant.components.cover import CoverEntity, CoverDeviceClass, CoverEntityFeature

from ..nhccoco.const import PROPERTY_ACTION_VALUE_OPEN, PROPERTY_ACTION_VALUE_CLOSE, PROPERTY_ACTION_VALUE_STOP
from ..nhccoco.devices.velux_action import CocoVeluxAction
from .nhc_entity import NHCBaseEntity


class Nhc2VeluxActionCoverEntity(NHCBaseEntity, CoverEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoVeluxAction, hub, gateway):
        """Initialize a cover."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

        self._attr_device_class = CoverDeviceClass.WINDOW
        self._attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
        self._attr_is_closed = None

    async def async_open_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_OPEN)
        self.schedule_update_ha_state()

    async def async_close_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_CLOSE)
        self.schedule_update_ha_state()

    async def async_stop_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_STOP)
        self.schedule_update_ha_state()
