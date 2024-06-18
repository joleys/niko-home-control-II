from homeassistant.components.lock import LockEntity

from ..nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction
from .nhc_entity import NHCBaseEntity


class Nhc2AccesscontrolActionLockEntity(NHCBaseEntity, LockEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoAccesscontrolAction, hub, gateway):
        """Initialize a lock sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

    @property
    def is_locked(self) -> bool:
        return self._device.is_doorlock_closed

    async def async_lock(self, **kwargs):
        return False

    async def async_unlock(self, **kwargs):
        self._device.open_doorlock(self._gateway)
        self.schedule_update_ha_state()
