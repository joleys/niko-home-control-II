"""Support for NHC2 lights."""
import logging
import json
from typing import List
from homeassistant.components.light import Light
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr

from .nhc2light import NHC2Light
from .nhc2 import NHC2
from .const import DOMAIN, BRAND, LIGHT

KEY_GATEWAY = 'nhc2_gateway'
KEY_LIGHTS = 'nhc2_lights'


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 lights based on a config entry."""
    hass.data.setdefault(KEY_LIGHTS, {})[config_entry.entry_id] : List[NHC2HassLight] = []

    @callback
    def process_lights(lights: List[NHC2Light]):
        active_uuids = []
        for light in hass.data[KEY_LIGHTS][config_entry.entry_id]:
            active_uuids.append(light.uuid)
        _LOGGER.debug('Now active UUIDs:'+json.dumps(active_uuids))
        _LOGGER.debug('Sent lights count:'+str(len(lights)))
        new_lights = []
        for light in lights:
            _LOGGER.debug('Processing light ' + light.name)
            if light.uuid in active_uuids:
                light_to_update = \
                    next(filter((
                        lambda x: x.uuid == light.uuid),
                        hass.data[KEY_LIGHTS][config_entry.entry_id]), None)
                light_to_update.nhc2_update(light)
                _LOGGER.debug('Updating light ' + light.name)
            else:
                new_light = NHC2HassLight(light, hass)
                hass.data[KEY_LIGHTS][config_entry.entry_id].append(new_light)
                new_lights.append(new_light)
                _LOGGER.debug('Adding new light ' + light.name)
        async_add_entities(new_lights)
        uuids_from_lights = list(map(lambda x: x.uuid, lights))
        uuids_to_remove = [i for i in uuids_from_lights + active_uuids if i not in uuids_from_lights]
        _LOGGER.debug('Now active lights UUIDs:'+json.dumps(uuids_from_lights))
        _LOGGER.debug('To remove lights UUIDs:'+json.dumps(uuids_to_remove))
        for uuid_to_remove in uuids_to_remove:
            light_to_remove = next(filter((
                lambda x: x.uuid == uuid_to_remove),
                hass.data[KEY_LIGHTS][config_entry.entry_id]), None)
            hass.add_job(light_to_remove.async_remove())
            hass.data[KEY_LIGHTS][config_entry.entry_id].remove(light_to_remove)


    gateway: NHC2 = hass.data[KEY_GATEWAY][config_entry.entry_id]
    gateway.get_lights(process_lights)


class NHC2HassLight(Light):
    """Representation of an NHC2 Light."""

    def __init__(self, nhc2light: NHC2Light, hass):
        self._nhc2light = nhc2light
        self._is_on = nhc2light.is_on()
        self._hass = hass

        def on_change():
            _LOGGER.debug('Got an NON UPDATED change message for' + nhc2light.name)
            update = self._is_on is not self._nhc2light.is_on()
            self._is_on = self._nhc2light.is_on()
            if update:
                self.schedule_update_ha_state()

        nhc2light.on_change = on_change


    def turn_off(self, **kwargs) -> None:
        pass

    def turn_on(self, **kwargs) -> None:
        pass

    async def async_turn_on(self, **kwargs):
        self._nhc2light.turn_on()
        self._is_on = True
        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        self._nhc2light.turn_off()
        self._is_on = False
        self.schedule_update_ha_state()

    def nhc2_update(self, nhc2light: NHC2Light):
        _LOGGER.debug('UPDATING light ' + nhc2light.name)
        def on_change():
            _LOGGER.debug('Got an updated on change message for' + nhc2light.name)
            update = self._is_on is not self._nhc2light.is_on()
            self._is_on = self._nhc2light.is_on()
            if update:
                self.schedule_update_ha_state()
        self._nhc2light = nhc2light
        nhc2light.on_change = on_change
        self.schedule_update_ha_state()

    @property
    def unique_id(self):
        return self._nhc2light.uuid

    @property
    def uuid(self):
        return self._nhc2light.uuid

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        return self._nhc2light.name

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
            'model': LIGHT,
            'sw_version': 'unknown',
            'via_hub': (DOMAIN, self._nhc2light.profile_creation_id),
        }
