from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.electricity_clamp_centralmeter import CocoElectricityClampCentralmeter
from .nhc_entity import NHCBaseEntity

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2ElectricityClampCentralmeterInvertedEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoElectricityClampCentralmeter, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid + '_inverted'
        self._attr_state = self._device.is_inverted
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Inverted'

    @property
    def is_on(self) -> bool:
        return self._device.is_inverted
