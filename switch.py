"""Support for NHC2 switches."""
import logging
from typing import List
from homeassistant.components.switch import SwitchDevice

from .nhc2entityprocessor import nhc2_entity_processor
from .nhc2switch import NHC2Switch
from .nhc2 import NHC2
from .const import DOMAIN, BRAND, SWITCH

KEY_GATEWAY = 'nhc2_gateway'
KEY_ENTITY = 'nhc2_switches'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id]: List = []
    gateway: NHC2 = hass.data[KEY_GATEWAY][config_entry.entry_id]
    _LOGGER.debug('Platform is starting')
    gateway.get_switches(
        nhc2_entity_processor(hass, config_entry, async_add_entities, KEY_ENTITY, lambda x: NHC2HassSwitch(x))
    )


class NHC2HassSwitch(SwitchDevice):
    """Representation of an NHC2 Switch."""

    def __init__(self, nhc2switch: NHC2Switch):
        self._nhc2switch = nhc2switch
        nhc2switch.on_change = self._on_change

    def _on_change(self):
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        pass

    def turn_on(self, **kwargs) -> None:
        pass

    async def async_turn_on(self, **kwargs):
        self._nhc2switch.turn_on()

    async def async_turn_off(self, **kwargs):
        self._nhc2switch.turn_off()

    def nhc2_update(self, nhc2switch: NHC2Switch):
        self._nhc2switch = nhc2switch
        nhc2switch.on_change = self._on_change
        self.schedule_update_ha_state()

    @property
    def unique_id(self):
        return self._nhc2switch.uuid

    @property
    def uuid(self):
        return self._nhc2switch.uuid

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        return self._nhc2switch.name

    @property
    def available(self):
        return self._nhc2switch.online

    @property
    def is_on(self):
        return self._nhc2switch.is_on

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self.unique_id)
            },
            'name': self.name,
            'manufacturer': BRAND,
            'model': SWITCH,
            'sw_version': 'unknown',
            'via_hub': (DOMAIN, self._nhc2switch.profile_creation_id),
        }
