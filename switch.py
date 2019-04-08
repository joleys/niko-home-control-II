"""Support for NHC2 switches."""
import logging
import json
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
        active_uuids = []
        for switch in hass.data[KEY_SWITCHES][config_entry.entry_id]:
            active_uuids.append(switch.uuid)
        _LOGGER.debug('Now active UUIDs:'+json.dumps(active_uuids))
        _LOGGER.debug('Sent switches count:' + str(len(switches)))
        new_switches = []
        for switch in switches:
            _LOGGER.debug('Processing switch ' + switch.name)
            if switch.uuid in active_uuids:
                switch_to_update = \
                    next(filter((
                        lambda x: x.uuid == switch.uuid),
                        hass.data[KEY_SWITCHES][config_entry.entry_id]), None)
                switch_to_update.nhc2_update(switch)
                _LOGGER.debug('Updating switch ' + switch.name)
            else:
                new_switch = NHC2HassSwitch(switch, hass)
                hass.data[KEY_SWITCHES][config_entry.entry_id].append(new_switch)
                new_switches.append(new_switch)
                _LOGGER.debug('Adding new switch ' + switch.name)
        async_add_entities(new_switches)
        uuids_from_switches = list(map(lambda x: x.uuid, switches))
        uuids_to_remove = [i for i in uuids_from_switches + active_uuids if i not in uuids_from_switches]
        _LOGGER.debug('Now active switches UUIDs:'+json.dumps(uuids_from_switches))
        _LOGGER.debug('To remove switches UUIDs:'+json.dumps(uuids_to_remove))
        for uuid_to_remove in uuids_to_remove:
            switch_to_remove = next(filter((
                lambda x: x.uuid == uuid_to_remove),
                hass.data[KEY_SWITCHES][config_entry.entry_id]), None)
            hass.add_job(switch_to_remove.async_remove())
            hass.data[KEY_SWITCHES][config_entry.entry_id].remove(switch_to_remove)

    gateway: NHC2 = hass.data[KEY_GATEWAY][config_entry.entry_id]
    gateway.get_switches(process_switches)


class NHC2HassSwitch(SwitchDevice):
    """Representation of an NHC2 Switch."""

    def __init__(self, nhc2switch: NHC2Switch, hass):
        self._nhc2switch = nhc2switch
        self._is_on = nhc2switch.is_on()
        self._hass = hass

        def on_change():
            _LOGGER.debug('Got an NON UPDATED change message for' + nhc2switch.name)
            update = self._is_on is not self._nhc2switch.is_on()
            self._is_on = self._nhc2switch.is_on()
            if update:
                self.schedule_update_ha_state()

        nhc2switch.on_change = on_change


    def turn_off(self, **kwargs) -> None:
        pass

    def turn_on(self, **kwargs) -> None:
        pass

    async def async_turn_on(self, **kwargs):
        self._nhc2switch.turn_on()
        self._is_on = True
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        self._nhc2switch.turn_off()
        self._is_on = False
        self.schedule_update_ha_state()

    def nhc2_update(self, nhc2switch: NHC2Switch):
        _LOGGER.debug('UPDATING switch ' + nhc2switch.name)
        def on_change():
            _LOGGER.debug('Got an updated on change message for' + nhc2switch.name)
            update = self._is_on is not self._nhc2switch.is_on()
            self._is_on = self._nhc2switch.is_on()
            if update:
                self.schedule_update_ha_state()
        self._nhc2switch = nhc2switch
        nhc2switch.on_change = on_change
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
    def is_on(self):
        return self._is_on

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
