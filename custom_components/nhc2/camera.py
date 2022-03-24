"""Support for Niko Home Control Access Control"""

import logging

import httpx
import voluptuous as vol

from homeassistant.components.camera import DEFAULT_CONTENT_TYPE, PLATFORM_SCHEMA, SUPPORT_STREAM, Camera
from homeassistant.exceptions import TemplateError


from . import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

from .nhccoco.coco import CoCo
from .nhccoco.coco_device_class import CoCoDeviceClass
from .nhccoco.coco_accesscontrol import CoCoAccessControl

from .const import DOMAIN, KEY_GATEWAY, BRAND
from .helpers import nhc2_entity_processor

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_accesscontrol'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 access control based on a config entry."""
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []
    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    _LOGGER.debug('Platform is starting')
    gateway.get_devices(CoCoDeviceClass.ACCESSCONTROL,
                        nhc2_entity_processor(hass,
                                              config_entry,
                                              async_add_entities,
                                              KEY_ENTITY,
                                              lambda x: NHC2HassAccessControl(x))
                        )

class NHC2HassAccessControl(Camera):
    """Implementation of NHC2 Camera."""
        
    def __init__(self, nhc2accesscontrol: CoCoAccessControl):
        """Initialize a camera."""
        nhc2accesscontrol.on_change = self._on_change
        self._nhc2accesscontrol = nhc2accesscontrol
        self._auth = httpx.BasicAuth(username='user', password='')
        self._stream_source = self._nhc2accesscontrol.stream_source

    @property
    def supported_features(self):
        """Return supported features for this camera."""
        return SUPPORT_STREAM

    @property
    def name(self):
        """Return the name of this device."""
        return self._nhc2accesscontrol.name

    async def stream_source(self):
        """Return the source of the stream."""
        if self._stream_source is None:
            return None

        try:
            return self._stream_source.async_render(parse_result=False)
        except TemplateError as err:
            _LOGGER.error("Error parsing template %s: %s", self._stream_source, err)
            return None