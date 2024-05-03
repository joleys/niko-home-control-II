from homeassistant.components.cover import CoverEntity, CoverDeviceClass, CoverEntityFeature, ATTR_POSITION

from ..nhccoco.const import PROPERTY_ACTION_VALUE_OPEN, PROPERTY_ACTION_VALUE_CLOSE, PROPERTY_ACTION_VALUE_STOP
from ..nhccoco.devices.gate_action import CocoGateAction
from ..nhccoco.devices.motor_action import CocoMotorAction
from ..nhccoco.devices.rolldownshutter_action import CocoRolldownshutterAction
from ..nhccoco.devices.sunblind_action import CocoSunblindAction
from ..nhccoco.devices.venetianblind_action import CocoVenetianblindAction


class Nhc2MotorActionCoverEntity(CoverEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoMotorAction, hub, gateway):
        """Initialize a light."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

        self._attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | \
                                        CoverEntityFeature.SET_POSITION | CoverEntityFeature.STOP


    @property
    def current_cover_position(self) -> int | None:
        return self._device.position

    @property
    def is_closed(self) -> bool:
        return self._device.position == 0

    @property
    def is_opening(self) -> bool:
        return self._device.is_opening

    @property
    def is_closing(self) -> bool:
        return self._device.is_closing

    @property
    def device_class(self) -> str:
        if isinstance(self._device, CocoGateAction):
            return CoverDeviceClass.GATE
        if isinstance(self._device, CocoRolldownshutterAction):
            return CoverDeviceClass.SHUTTER
        if isinstance(self._device, CocoSunblindAction):
            return CoverDeviceClass.BLIND
        if isinstance(self._device, CocoVenetianblindAction):
            return CoverDeviceClass.SHUTTER

        return None

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_open_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_OPEN)
        self.on_change()

    async def async_close_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_CLOSE)
        self.on_change()

    async def async_stop_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_STOP)
        self.on_change()

    async def async_set_cover_position(self, **kwargs):
        self._device.set_position(self._gateway, kwargs.get(ATTR_POSITION))
        self.on_change()
