"""Support for NHC2 lights."""
import logging
from typing import Any, Optional

from homeassistant.components.fan import FanEntity, SUPPORT_SET_SPEED
from .coco import CoCo
from .coco_device_class import CoCoDeviceClass
from .coco_fan import CoCoFan
from .coco_fan_speed import CoCoFanSpeed
from .coco_switched_fan import CoCoSwitchedFan

from .const import DOMAIN, KEY_GATEWAY, BRAND, FAN
from .helpers import nhc2_entity_processor

from homeassistant.util.percentage import ordered_list_item_to_percentage, percentage_to_ordered_list_item

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_fans'

SPEED_BOOST = 'boost'
SPEED_HIGH = 100
SPEED_LOW = 10
SPEED_MEDIUM = 50

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 fan based on a config entry."""
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


class NHC2HassFan(FanEntity):
    """Representation of an NHC2 Fan."""

    def __init__(self, nhc2fan: CoCoFan):
        """Initialize a fan."""
        self._nhc2fan = nhc2fan
        self._fan_speeds = self._nhc2fan.fan_speeds
        self._percentage = ordered_list_item_to_percentage(self._fan_speeds, self._nhc2fan.fan_speed)
        nhc2fan.on_change = self._on_change

    def set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        self._nhc2fan.change_speed(percentage_to_ordered_list_item(self._fan_speeds, percentage))

    def turn_on(self, speed: Optional[str] = None, percentage: Optional[int] = None, preset_mode: Optional[str] = None, **kwargs: Any) -> None:
        """Turn on the fan."""
        if percentage is not None:
            self.set_percentage(percentage)

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the fan off."""
        pass

    def _on_change(self):
        self._percentage = ordered_list_item_to_percentage(self._fan_speeds, self._nhc2fan.fan_speed)
        self.schedule_update_ha_state()

    def nhc2_update(self, nhc2fan: CoCoFan):
        """Update the NHC2 fan with a new object."""
        self._nhc2fan = nhc2fan
        nhc2fan.on_change = self._on_change
        self.schedule_update_ha_state()

    @property
    def percentage(self) -> int:
        """Return the current speed percentage."""
        return self._percentage

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return len(self._fan_speeds)

    @property
    def unique_id(self):
        """Return the fan's UUID."""
        return self._nhc2fan.uuid

    @property
    def uuid(self):
        """Return the fan's UUID."""
        return self._nhc2fan.uuid

    @property
    def should_poll(self):
        """Return false, since the fan will push state."""
        return False

    @property
    def name(self):
        """Return the fan's name."""
        return self._nhc2fan.name

    @property
    def available(self):
        """Return true if the fan is online."""
        #return self._nhc2fan.online
        return True

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