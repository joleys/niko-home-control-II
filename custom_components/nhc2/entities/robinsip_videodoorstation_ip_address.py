from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.robinsip_videodoorstation import CocoRobinsipVideodoorstation


class Nhc2RobinsipVideodoorstationIpAddressEntity(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoRobinsipVideodoorstation, hub, gateway):
        """Initialize a sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_ip_address'
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

        self._attr_native_value = self._device.ip_address_readable
        self._attr_state_class = None
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'IP Address'

    @property
    def state(self) -> str:
        return self._device.ip_address_readable

    def on_change(self):
        self.schedule_update_ha_state()
