from homeassistant.components.lock import LockEntity

from ..nhccoco.devices.bellbutton_action import CocoBellbuttonAction
from .nhc_entity import NHCBaseEntity


class Nhc2BellbuttonActionLockEntity(NHCBaseEntity, LockEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoBellbuttonAction, hub, gateway):
        """Initialize a lock sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid

    @property
    def is_locked(self) -> bool:
        return self._device.is_doorlock_closed

    def lock(self, **kwargs):
        """Pass - not in use."""
        pass

    async def async_lock(self, **kwargs):
        """Pass - not in use."""
        pass

    def unlock(self, **kwargs):
        """Pass - not in use."""
        pass

    async def async_unlock(self, **kwargs):
        self._device.open_doorlock(self._gateway)
        self.schedule_update_ha_state()
