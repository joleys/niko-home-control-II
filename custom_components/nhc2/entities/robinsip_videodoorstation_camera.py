import aiohttp
from homeassistant.components.mjpeg.camera import MjpegCamera
from homeassistant.const import HTTP_BASIC_AUTHENTICATION

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.robinsip_videodoorstation import CocoRobinsipVideodoorstation

from PIL import ImageFile

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2RobinsipVideodoorstationCameraEntity(MjpegCamera):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoRobinsipVideodoorstation, hub, gateway):
        """Initialize a camera sensor."""

        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False
        self._attr_is_streaming = True

        self._username = 'admin'
        self._password = '123qwe'
        self._mjpeg_url = f'http://{self._device.ip_address_readable}{self._device.mjpeg_uri}'
        self._still_image_url = f'http://{self._device.ip_address_readable}{self._device.tn_uri}'

        self._camera = MjpegCamera.__init__(
            self,
            mjpeg_url=self._mjpeg_url,
            still_image_url=self._still_image_url,
            authentication=HTTP_BASIC_AUTHENTICATION,
            username=self._username,
            password=self._password,
        )

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

    async def async_camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        # This is a workaround for the fact that the camera sometimes returns stills of 1x1 pixels
        counter = 0
        while counter < 10:
            counter += 1

            image = await MjpegCamera.async_camera_image(self, width, height)
            p = ImageFile.Parser()
            p.feed(image)
            _LOGGER.debug(f'Image size for still image is: {p.image.size}')

            if p.image is None:
                image = None
                continue

            if p.image.size != (1, 1):
                break

        return image
