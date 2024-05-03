from homeassistant.components.lock import LockEntity

from ..nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction


class Nhc2AccesscontrolActionLockEntity(LockEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoAccesscontrolAction, hub, gateway):
        """Initialize a lock sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

    @property
    def is_locked(self) -> bool:
        return self._device.is_doorlock_closed

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_lock(self, **kwargs):
        return False

    async def async_unlock(self, **kwargs):
        self._device.open_doorlock(self._gateway)
        self.on_change()
