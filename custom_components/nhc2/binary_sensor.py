"""Support for NHC2 Virtual Device."""
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity

from .nhccoco.coco import CoCo
from .nhccoco.coco_virtual import CoCoVirtual
from .nhccoco.coco_device_class import CoCoDeviceClass

from .const import DOMAIN, KEY_GATEWAY, BRAND
from .helpers import nhc2_entity_processor

KEY_GATEWAY = KEY_GATEWAY

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 virtual devices based on a config entry."""
    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    _LOGGER.debug('Platform is starting')
    hass.data.setdefault('nhc2_virtual', {})[config_entry.entry_id] = []
    gateway.get_devices(CoCoDeviceClass.VIRTUAL,
                        nhc2_entity_processor(hass,
                                              config_entry,
                                              async_add_entities,
                                              'nhc2_virtual',
                                              lambda x: NHC2HassBinarySensor(x))
                        )


class NHC2HassBinarySensor(BinarySensorEntity):
    """Representation of an NHC2 Virtual Device."""

    def __init__(self, nhc2virtual: CoCoVirtual):
        """Initialize a virtual device."""
        self._nhc2virtual = nhc2virtual
        self._is_on = self._nhc2virtual.is_on
        nhc2virtual.on_change = self._on_change

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._is_on

    def _on_change(self):
        self._is_on = self._nhc2virtual.is_on
        self.schedule_update_ha_state()

    def nhc2_update(self, nhc2virtual: CoCoVirtual):
        """Update the NHC2 Virtual with a new object."""
        self._nhc2virtual = nhc2virtual
        nhc2virtual.on_change = self._on_change
        self.schedule_update_ha_state()

    @property
    def unique_id(self):
        """Return the virtual device UUID."""
        return self._nhc2virtual.uuid

    @property
    def uuid(self):
        """Return the virtual device UUID."""
        return self._nhc2virtual.uuid

    @property
    def should_poll(self):
        """Return false, since the virtual device will push state."""
        return False

    @property
    def name(self):
        """Return the virtual device name."""
        return self._nhc2virtual.name

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self.unique_id)
            },
            'name': self.name,
            'manufacturer': BRAND,
            'via_hub': (DOMAIN, self._nhc2virtual.profile_creation_id),
        }
