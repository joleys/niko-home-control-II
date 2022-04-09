"""Support for NHC2 covers."""
import logging

from homeassistant.components.cover import CoverEntity, SUPPORT_OPEN, SUPPORT_CLOSE, SUPPORT_STOP, SUPPORT_SET_POSITION, \
    ATTR_POSITION, DEVICE_CLASS_SHUTTER, DEVICE_CLASS_BLIND, DEVICE_CLASS_GATE
from .coco import CoCo
from .coco_device_class import CoCoDeviceClass
from .coco_shutter import CoCoShutter

from .const import DOMAIN, KEY_GATEWAY, BRAND, COVER, ROLL_DOWN_SHUTTER, SUN_BLIND, GATE, VENETIAN_BLIND
from .helpers import nhc2_entity_processor

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_covers'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 covers based on a config entry."""
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []
    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    _LOGGER.debug('Platform is starting')
    gateway.get_devices(CoCoDeviceClass.SHUTTERS,
                        nhc2_entity_processor(hass,
                                              config_entry,
                                              async_add_entities,
                                              KEY_ENTITY,
                                              lambda x: NHC2HassCover(x))
                        )


class NHC2HassCover(CoverEntity):
    """Representation of an NHC2 Cover."""

    def __init__(self, nhc2shutter: CoCoShutter):
        """Initialize a switch."""
        self._nhc2shutter = nhc2shutter
        self._position = nhc2shutter.position
        self._is_closed = (nhc2shutter.position == 0)
        nhc2shutter.on_change = self._on_change

    @property
    def current_cover_position(self):
        """Return current position of cover. 0 is closed, 100 is open."""
        return self._position

    @property
    def device_class(self):
        model = self._nhc2shutter.model
        if model == ROLL_DOWN_SHUTTER:
            return DEVICE_CLASS_SHUTTER
        if model == SUN_BLIND:
            return DEVICE_CLASS_BLIND
        if model == GATE:
            return DEVICE_CLASS_GATE
        if model == VENETIAN_BLIND:
            return DEVICE_CLASS_SHUTTER
        # If model not known, we choose 'generic' by returning None
        return None

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP | SUPPORT_SET_POSITION

    def _on_change(self):
        self._is_closed = (self._nhc2shutter.position == 0)
        self._position = self._nhc2shutter.position
        self.schedule_update_ha_state()

    def open_cover(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def close_cover(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def stop_cover(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def set_cover_position(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    async def async_open_cover(self, **kwargs):
        """Instruct the cover to open."""
        self._nhc2shutter.open()

    async def async_close_cover(self, **kwargs):
        """Instruct the cover to close."""
        self._nhc2shutter.close()

    async def async_stop_cover(self, **kwargs):
        """Instruct the cover to stop."""
        self._nhc2shutter.stop()

    async def async_set_cover_position(self, **kwargs):
        """Instruct the cover to stop."""
        self._nhc2shutter.set_position(kwargs[ATTR_POSITION])

    def nhc2_update(self, nhc2shutter: CoCoShutter):
        """Update the NHC2 switch with a new object."""
        self._nhc2shutter = nhc2shutter
        nhc2shutter.on_change = self._on_change
        self.schedule_update_ha_state()

    @property
    def unique_id(self):
        """Return the lights UUID."""
        return self._nhc2shutter.uuid

    @property
    def uuid(self):
        """Return the lights UUID."""
        return self._nhc2shutter.uuid

    @property
    def should_poll(self):
        """Return false, since the cover will push state."""
        return False

    @property
    def name(self):
        """Return the lights name."""
        return self._nhc2shutter.name

    @property
    def available(self):
        """Return true if the light is online."""
        return self._nhc2shutter.online

    @property
    def is_closed(self):
        """Return true if the light is on."""
        return self._is_closed

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self.unique_id)
            },
            'name': self.name,
            'manufacturer': BRAND,
            'model': COVER,
            'via_hub': (DOMAIN, self._nhc2shutter.profile_creation_id),
        }
