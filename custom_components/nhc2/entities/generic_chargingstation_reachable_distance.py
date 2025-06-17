from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.const import UnitOfLength

from ..nhccoco.devices.generic_chargingstation import CocoGenericChargingstation
from .nhc_entity import NHCBaseEntity


class Nhc2GenericChargingstationReachableDistanceEntity(NHCBaseEntity, NumberEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericChargingstation, hub, gateway):
        """Initialize a number entity."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_reachable_distance'

        self._attr_device_class = NumberDeviceClass.DISTANCE
        min_value, max_value, step = self._device.reachable_distance_range
        self._attr_native_max_value = max_value
        self._attr_native_min_value = min_value
        self._attr_native_step = step
        self._attr_native_unit_of_measurement = UnitOfLength.KILOMETERS

    @property
    def name(self) -> str:
        return 'Reachable Distance'

    @property
    def native_value(self) -> float:
        return self._device.reachable_distance

    async def async_set_native_value(self, value: float) -> None:
        self._device.set_reachable_distance(self._gateway, value)
        self.schedule_update_ha_state()
