from homeassistant.components.binary_sensor import BinarySensorEntity

from ..nhccoco.devices.hvacthermostat_hvac import CocoHvacthermostatHvac
from .nhc_entity import NHCBaseEntity


class Nhc2HvacthermostatHvacHvacOnEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoHvacthermostatHvac, hub, gateway):
        """Initialize a switch sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_hvac_on'

    @property
    def name(self) -> str:
        return 'HVAC on'

    @property
    def is_on(self) -> bool:
        return self._device.is_hvac_on
