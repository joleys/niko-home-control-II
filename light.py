"""Support for NHC2 switches."""
import logging
from typing import List
from homeassistant.components.light import Light
from homeassistant.core import callback

from .nhc2light import NHC2Light
from .nhc2 import NHC2
from .const import DOMAIN, BRAND, LIGHT

KEY_GATEWAY = 'nhc2_gateway'
KEY_LIGHTS = 'nhc2_lights'




async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 switches based on a config entry."""
    hass.data.setdefault(KEY_LIGHTS, {})[config_entry.entry_id] : List[NHC2HassLight] = []

    @callback
    def process_lights(lights: List[NHC2Light]):
        if len(hass.data[KEY_LIGHTS][config_entry.entry_id]) == 0:
            for light in lights:
                hass.data[KEY_LIGHTS][config_entry.entry_id].append(NHC2HassLight(light))
            async_add_entities(hass.data[KEY_LIGHTS][config_entry.entry_id])

    gateway: NHC2 = hass.data[KEY_GATEWAY][config_entry.entry_id]
    gateway.get_lights(process_lights)


class NHC2HassLight(Light):
    """Representation of an NHC2 Light."""

    def __init__(self, nhc2light: NHC2Light):
        self._nhc2light = nhc2light

        def on_change():
            self.async_write_ha_state()

        nhc2light.on_change = on_change


    @property
    def unique_id(self):
        return self._nhc2light.uuid

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        return self._nhc2light.name

    @property
    def is_on(self):
        return self._nhc2light.is_on()

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
    def turn_off(self, **kwargs) -> None:
        pass

    def turn_on(self, **kwargs) -> None:
        pass

    async def async_turn_on(self, **kwargs):
        self._nhc2light.turn_on()

    async def async_turn_off(self, **kwargs):
        self._nhc2light.turn_off()
