"""Support for NHC2 lights."""
import logging

from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, ATTR_BRIGHTNESS
from .coco import CoCoLight, CoCo
from .coco_device_class import CoCoDeviceClass

from .const import DOMAIN, KEY_GATEWAY, BRAND, LIGHT
from .helpers import nhc2_entity_processor

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_lights'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 lights based on a config entry."""
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []
    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    _LOGGER.debug('Platform is starting')
    gateway.get_devices(CoCoDeviceClass.LIGHTS,
                        nhc2_entity_processor(hass,
                                              config_entry,
                                              async_add_entities,
                                              KEY_ENTITY,
                                              lambda x: NHC2HassLight(x))
                        )


class NHC2HassLight(LightEntity):
    """Representation of an NHC2 Light."""

    def __init__(self, nhc2light: CoCoLight, optimistic=True):
        """Initialize a light."""
        self._nhc2light = nhc2light
        self._optimistic = optimistic
        self._is_on = nhc2light.is_on
        if self._nhc2light.support_brightness:
            if self._is_on is False:
                self._brightness = 0
            else:
                self._brightness = round(self._nhc2light.brightness * 2.55)
        else:
            self._brightness = None
        nhc2light.on_change = self._on_change

    def _on_change(self):
        self._is_on = self._nhc2light.is_on
        if self._nhc2light.support_brightness:
            if self._is_on is False:
                self._brightness = 0
            else:
                self._brightness = round(self._nhc2light.brightness * 2.55)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    def turn_on(self, **kwargs) -> None:
        """Pass - not in use."""
        pass

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        self._nhc2light.turn_on()
        brightness = kwargs.get(ATTR_BRIGHTNESS)

        if self._nhc2light.support_brightness and brightness is not None:
            self._nhc2light.set_brightness(round((brightness) / 2.55))

        if self._optimistic:
            self._is_on = True
            self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._nhc2light.turn_off()
        if self._optimistic:
            self._is_on = False
            self.schedule_update_ha_state()

    def nhc2_update(self, nhc2light: CoCoLight):
        """Update the NHC2 light with a new object."""
        self._nhc2light = nhc2light
        nhc2light.on_change = self._on_change
        self.schedule_update_ha_state()

    @property
    def unique_id(self):
        """Return the lights UUID."""
        return self._nhc2light.uuid

    @property
    def uuid(self):
        """Return the lights UUID."""
        return self._nhc2light.uuid

    @property
    def should_poll(self):
        """Return false, since the light will push state."""
        return False

    @property
    def name(self):
        """Return the lights name."""
        return self._nhc2light.name

    @property
    def available(self):
        """Return true if the light is online."""
        return self._nhc2light.online

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def is_on(self):
        """Return true if the light is on."""
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
            'via_hub': (DOMAIN, self._nhc2light.profile_creation_id),
        }

    @property
    def supported_features(self):
        """Return supported features."""
        if self._nhc2light.support_brightness:
            return SUPPORT_BRIGHTNESS
        return 0
