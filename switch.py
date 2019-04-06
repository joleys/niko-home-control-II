"""Support for NHC2 switches."""
import logging
from typing import List
from homeassistant.components.switch import SwitchDevice
from homeassistant.core import callback

from .nhc2switch import NHC2Switch
from .nhc2 import NHC2
from .const import DOMAIN, BRAND, SWITCH

KEY_GATEWAY = 'nhc2_gateway'
KEY_SWITCHES = 'nhc2_switches'


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 switches based on a config entry."""
    hass.data.setdefault(KEY_SWITCHES, {})[config_entry.entry_id] : List[NHC2HassSwitch] = []

    @callback
    def process_switches(switches: List[NHC2Switch]):
        if len(hass.data[KEY_SWITCHES][config_entry.entry_id]) == 0:
            for switch in switches:
                hass.data[KEY_SWITCHES][config_entry.entry_id].append(NHC2HassSwitch(switch))
            async_add_entities(hass.data[KEY_SWITCHES][config_entry.entry_id])
    gateway: NHC2 = hass.data[KEY_GATEWAY][config_entry.entry_id]
    gateway.get_switches(process_switches)


class NHC2HassSwitch(SwitchDevice):
    """Representation of an NHC2 Switch."""

    def __init__(self, nhc2switch: NHC2Switch):
        self._nhc2switch = nhc2switch

        def on_change():
            _LOGGER.debug('Requesting update')
            self.schedule_update_ha_state()

        nhc2switch.on_change = on_change


    @property
    def unique_id(self):
        return self._nhc2switch.uuid

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        return self._nhc2switch.name

    @property
    def is_on(self):
        return self._nhc2switch.is_on()

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
    def turn_off(self, **kwargs) -> None:
        pass

    def turn_on(self, **kwargs) -> None:
        pass

    async def async_turn_on(self, **kwargs):
        self._nhc2switch.turn_on()

    async def async_turn_off(self, **kwargs):
        self._nhc2switch.turn_off()
