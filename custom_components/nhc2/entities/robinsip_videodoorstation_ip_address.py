from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.robinsip_videodoorstation import CocoRobinsipVideodoorstation
from .nhc_entity import NHCBaseEntity


class Nhc2RobinsipVideodoorstationIpAddressEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoRobinsipVideodoorstation, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_ip_address'

        self._attr_native_value = self._device.ip_address_readable
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'IP Address'

    @property
    def state(self) -> str:
        return self._device.ip_address_readable
