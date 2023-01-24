from homeassistant.components.binary_sensor import BinarySensorEntity

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction


class Nhc2AccesscontrolActionDeclineCallAppliedOnAllDevicesEntity(BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoAccesscontrolAction, hub, gateway):
        """Initialize a binary sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_accesscontrol_decline_call_applied_on_all_devices'
        self._attr_should_poll = False

        self._attr_state = self._device.is_decline_call_applied_on_all_devices
        self._attr_state_class = None

    @property
    def name(self) -> str:
        return 'AccessControl Basic State'

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': BRAND,
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def is_on(self) -> bool:
        return self._device.is_decline_call_applied_on_all_devices

    def on_change(self):
        self.schedule_update_ha_state()
