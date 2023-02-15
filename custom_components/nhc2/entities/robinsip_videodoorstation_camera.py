from homeassistant.components.camera import Camera, CameraEntityFeature, StreamType

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.robinsip_videodoorstation import CocoRobinsipVideodoorstation


class Nhc2RobinsipVideodoorstationCameraEntity(Camera):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoRobinsipVideodoorstation, hub, gateway):
        # I don't know why, but this is needed to make it work...
        Camera.__init__(self)
        """Initialize a camera sensor."""

        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        self._attr_name = self._device.name
        self._attr_supported_features = CameraEntityFeature.STREAM
        self._attr_is_streaming = True
        self._attr_stream_type = StreamType.HLS

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

    async def stream_source(self) -> str:
        return f'http://admin:123qwe@{self._device.ip_address_readable}{self._device.mjpeg_uri}'
