from datetime import time

from homeassistant.components.time import TimeEntity

from ..nhccoco.devices.generic_chargingstation import CocoGenericChargingstation
from .nhc_entity import NHCBaseEntity


class Nhc2GenericChargingstationNextChargingTimeEntity(NHCBaseEntity, TimeEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericChargingstation, hub, gateway):
        """Initialize a time entity."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_next_charging_time'

    @property
    def name(self) -> str:
        return 'Next Charging Time'

    @property
    def state(self) -> time:
        return self._device.next_charging_time

    async def async_set_value(self, value: time) -> None:
        self._device.set_next_charging_time(self._gateway, value)
        self.schedule_update_ha_state()

