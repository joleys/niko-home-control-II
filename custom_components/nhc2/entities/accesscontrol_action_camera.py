from homeassistant.components.camera import Camera, CameraEntityFeature

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.accesscontrol_action import CocoAccesscontrolAction


class Nhc2AccesscontrolActionCameraEntity(Camera):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoAccesscontrolAction, hub, gateway):
        """Initialize a lock sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        self._attr_brand = BRAND
        self._attr_model = str.title(f'{self._device.model} ({self._device.type})')
        self._attr_supported_features = CameraEntityFeature.STREAM

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

    def on_change(self):
        self.schedule_update_ha_state()

    async def stream_source(self) -> str | None:
        return f'http://user@{self._gateway.address}:15110'
