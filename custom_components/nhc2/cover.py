"""Support for NHC2 covers."""
import logging
from telnetlib import GA

from homeassistant.components.cover import CoverEntity, SUPPORT_OPEN, SUPPORT_CLOSE, SUPPORT_STOP, SUPPORT_SET_POSITION, \
    ATTR_POSITION, DEVICE_CLASS_SHUTTER, DEVICE_CLASS_BLIND, DEVICE_CLASS_GATE, DEVICE_CLASS_GARAGE
from .nhccoco.coco import CoCo
from .nhccoco.coco_device_class import CoCoDeviceClass
from .nhccoco.coco_cover import CoCoCover

from .const import DOMAIN, GARAGE_DOOR, KEY_GATEWAY, BRAND, COVER, ROLL_DOWN_SHUTTER, SUN_BLIND, GATE, VENETIAN_BLIND
from .helpers import nhc2_entity_processor

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_covers'

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 covers based on a config entry."""
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []
    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    _LOGGER.debug('Platform is starting')
    gateway.get_devices(CoCoDeviceClass.COVERS,
                        nhc2_entity_processor(hass,
                                              config_entry,
                                              async_add_entities,
                                              KEY_ENTITY,
                                              lambda x: NHC2HassCover(x, "alfa"))
                        )

class NHC2HassCover(CoverEntity):
    """Representation of an NHC2 Cover (shutters, blinds, garage doors)."""

    def __init__(self, nhc2cover: CoCoCover, parm):
        """Initialize a cover."""
        self._nhc2cover = nhc2cover
        self._status = self._nhc2cover.status
        self._model = self._nhc2cover.model
        self._position = self._nhc2cover.position
        nhc2cover.on_change = self._on_change
        _LOGGER.debug('Function argument: %s', parm)

    @property
    def is_closed(self):
        """Return True if cover is closed, else None."""
        if self._position == 'CLOSED':
            return True
        if self._position == 'OPEN':
            return False
        return None

    @property
    def is_closing(self):
        """Return if the cover is closing or not."""
        return self._position == 'CLOSING'

    @property
    def is_opening(self):
        """Return if the cover is opening or not."""
        return self._position == 'OPENING'

    @property
    def current_cover_position(self):
        """Return current position of cover. 0 is closed, 100 is open."""
        if self._model == GARAGE_DOOR:
            return None
        return self._position

    @property
    def device_class(self):
        if self._model == ROLL_DOWN_SHUTTER:
            return DEVICE_CLASS_SHUTTER
        if self._model == SUN_BLIND:
            return DEVICE_CLASS_BLIND
        if self._model == GATE:
            return DEVICE_CLASS_GATE
        if self._model == VENETIAN_BLIND:
            return DEVICE_CLASS_SHUTTER
        if self._model == GARAGE_DOOR:
            return DEVICE_CLASS_GARAGE
        # If model not known, we choose 'generic' by returning None
        return None

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        if self._model == GARAGE_DOOR:
            return SUPPORT_OPEN | SUPPORT_CLOSE
        else:
            return SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP | SUPPORT_SET_POSITION

    def _on_change(self):
        self._status = self._nhc2cover.status
        self._position = self._nhc2cover.position
        self.schedule_update_ha_state()
        _LOGGER.debug('update cover state: %s', self._status)
        _LOGGER.debug('update cover position: %s', self._position)

    async def async_open_cover(self, **kwargs):
        """Instruct the cover to open."""
        self._nhc2cover.open()

    async def async_close_cover(self, **kwargs):
        """Instruct the cover to close."""
        self._nhc2cover.close()

    async def async_stop_cover(self, **kwargs):
        """Instruct the cover to stop."""
        self._nhc2cover.stop()
    
    async def async_set_cover_position(self, **kwargs):
        """Instruct the cover to stop."""
        self._nhc2cover.set_position(kwargs[ATTR_POSITION])

    @property
    def unique_id(self):
        """Return the cover's UUID."""
        return self._nhc2cover.uuid

    @property
    def uuid(self):
        """Return the cover's UUID."""
        return self._nhc2cover.uuid

    @property
    def should_poll(self):
        """Return false, since the cover will push state."""
        return False

    @property
    def name(self):
        """Return the cover's name."""
        return self._nhc2cover.name

    @property
    def available(self):
        """Return true if the cover is online."""
        if self._model == GARAGE_DOOR:
            return True
            #return self._nhc2cover.online
            #force True > asked NIKO for additional information why the controller returns False
        else:
            return self._nhc2cover.online

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
            'via_hub': (DOMAIN, self._nhc2cover.profile_creation_id),
        }