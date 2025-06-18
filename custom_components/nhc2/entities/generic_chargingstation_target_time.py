from datetime import time

from homeassistant.components.time import TimeEntity

from ..nhccoco.devices.generic_chargingstation import CocoGenericChargingstation
from .nhc_entity import NHCBaseEntity


class Nhc2GenericChargingstationTargetTimeEntity(NHCBaseEntity, TimeEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericChargingstation, hub, gateway):
        """Initialize a time entity."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_target_time'

    @property
    def name(self) -> str:
        return 'Target Time'

    @property
    def state(self) -> time:
        return self._device.target_time

    async def async_set_value(self, value: time) -> None:
        self._device.set_target_time(self._gateway, value)
        self.schedule_update_ha_state()

