"""Support for NHC2 lights."""
import logging
from typing import Any

from homeassistant.components.fan import FanEntity, SUPPORT_SET_SPEED
from .coco import CoCo
from .coco_device_class import CoCoDeviceClass
from .coco_fan import CoCoFan
from .coco_fan_speed import CoCoFanSpeed
from .coco_switched_fan import CoCoSwitchedFan

from .const import DOMAIN, KEY_GATEWAY, BRAND, FAN
from .helpers import nhc2_entity_processor

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_fans'

SPEED_BOOST = 'boost'
SPEED_HIGH = 100
SPEED_LOW = 10
SPEED_MEDIUM = 50

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 lights based on a config entry."""
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []
    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    _LOGGER.debug('Platform is starting')
    gateway.get_devices(CoCoDeviceClass.FANS,
                        nhc2_entity_processor(hass,
                                              config_entry,
                                              async_add_entities,
                                              KEY_ENTITY,
                                              lambda x: NHC2HassFan(x))
                        )
    gateway.get_devices(CoCoDeviceClass.SWITCHED_FANS,
                        nhc2_entity_processor(hass,
                                              config_entry,
                                              async_add_entities,
                                              KEY_ENTITY,
                                              lambda x: NHC2HassSwitchedFan(x))
                        )


class NHC2HassFan(FanEntity):
    """Representation of an NHC2 Fan."""

    def __init__(self, nhc2fan: CoCoFan):
        """Initialize a light."""
        self._nhc2fan = nhc2fan
        self._fan_speed = self._convert_fan_speed_nhc22hass(nhc2fan.fan_speed)
        nhc2fan.on_change = self._on_change

    def set_speed(self, speed: str) -> None:
        nhc2speed = self._convert_fan_speed_hass2nhc2(speed)
        self._nhc2fan.change_speed(nhc2speed)

    def set_direction(self, direction: str) -> None:
        pass

    def turn_on(self, speed: str = None, **kwargs) -> None:
        if speed is not None:
            self.set_speed(speed)

    def turn_off(self, **kwargs: Any) -> None:
        pass

    def _on_change(self):
        self._fan_speed = self._convert_fan_speed_nhc22hass(self._nhc2fan.fan_speed)
        self.schedule_update_ha_state()

    @property
    def speed(self) -> str:
        """Return the current speed."""
        return self._fan_speed

    @property
    def speed_list(self) -> list:
        """Get the list of available speeds."""
        return [SPEED_LOW,
                SPEED_MEDIUM,
                SPEED_HIGH,
                SPEED_BOOST]

    @property
    def unique_id(self):
        """Return the lights UUID."""
        return self._nhc2fan.uuid

    @property
    def uuid(self):
        """Return the lights UUID."""
        return self._nhc2fan.uuid

    @property
    def should_poll(self):
        """Return false, since the light will push state."""
        return False

    @property
    def name(self):
        """Return the lights name."""
        return self._nhc2fan.name

    @property
    def available(self):
        """Return true if the light is online."""
        return self._nhc2fan.online

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self.unique_id)
            },
            'name': self.name,
            'manufacturer': BRAND,
            'model': FAN,
            'via_hub': (DOMAIN, self._nhc2fan.profile_creation_id),
        }

    @property
    def supported_features(self):
        """Return supported features."""
        return SUPPORT_SET_SPEED

    # Helper functions

    def _convert_fan_speed_nhc22hass(self, fan_speed: CoCoFanSpeed) -> str:
        if fan_speed == CoCoFanSpeed.HIGH:
            return SPEED_HIGH
        if fan_speed == CoCoFanSpeed.LOW:
            return SPEED_LOW
        if fan_speed == CoCoFanSpeed.MEDIUM:
            return SPEED_MEDIUM
        if fan_speed == CoCoFanSpeed.BOOST:
            return SPEED_BOOST

    def _convert_fan_speed_hass2nhc2(self, fan_speed: str) -> CoCoFanSpeed:
        if fan_speed == SPEED_HIGH:
            return CoCoFanSpeed.HIGH
        if fan_speed == SPEED_LOW:
            return CoCoFanSpeed.LOW
        if fan_speed == SPEED_MEDIUM:
            return CoCoFanSpeed.MEDIUM
        if fan_speed == SPEED_BOOST:
            return CoCoFanSpeed.BOOST


class NHC2HassSwitchedFan(FanEntity):
    """Representation of an NHC2 Fan."""

    def __init__(self, nhc2switched_fan: CoCoSwitchedFan):
        """Initialize a light."""
        self._nhc2switched_fan = nhc2switched_fan
        self._is_on = nhc2switched_fan.is_on
        nhc2switched_fan.on_change = self._on_change

    def set_speed(self, speed: str) -> None:
        pass

    def set_direction(self, direction: str) -> None:
        pass

    def turn_on(self, speed: str = None, **kwargs) -> None:
        self._nhc2switched_fan.turn_on()

    def turn_off(self, **kwargs: Any) -> None:
        self._nhc2switched_fan.turn_off()

    def _on_change(self):
        self._is_on = self._nhc2switched_fan.is_on
        self.schedule_update_ha_state()

    @property
    def unique_id(self):
        """Return the lights UUID."""
        return self._nhc2switched_fan.uuid

    @property
    def uuid(self):
        """Return the lights UUID."""
        return self._nhc2switched_fan.uuid

    @property
    def should_poll(self):
        """Return false, since the light will push state."""
        return False

    @property
    def name(self):
        """Return the lights name."""
        return self._nhc2switched_fan.name

    @property
    def available(self):
        """Return true if the light is online."""
        return self._nhc2switched_fan.online

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self.unique_id)
            },
            'name': self.name,
            'manufacturer': BRAND,
            'model': FAN,
            'via_hub': (DOMAIN, self._nhc2switched_fan.profile_creation_id),
        }
