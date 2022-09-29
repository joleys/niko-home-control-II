import logging
from homeassistant.components.button import ButtonEntity
from .nhccoco.coco_device_class import CoCoDeviceClass

from .helpers import nhc2_entity_processor
from .nhccoco.coco import CoCo
from .nhccoco.coco_button import CoCoButton

from .const import DOMAIN, KEY_GATEWAY, BRAND, BUTTON

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_buttons'

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 buttons based on a config entry."""
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []
    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    _LOGGER.debug('Platform is starting')
    gateway.get_devices(CoCoDeviceClass.BUTTONS,
        nhc2_entity_processor(hass,
                              config_entry,
                              async_add_entities,
                              KEY_ENTITY,
                              lambda x: NHC2HassButton(x))
    )


class NHC2HassButton(ButtonEntity):
    def __init__(self, nhc2button: CoCoButton, optimistic=True):
        """Initialize a button."""
        self._nhc2button = nhc2button
        self._optimistic = optimistic
        nhc2button.on_change = self._on_change

    def _on_change(self):
        self._is_on = self._nhc2button.is_on
        self.schedule_update_ha_state()

    def press(self, **kwargs) -> None:
        self._nhc2button.press()

    def nhc2_update(self, nhc2button: CoCoButton):
        """Update the NHC2 button with a new object."""
        self._nhc2button = nhc2button
        nhc2button.on_change = self._on_change
        self.schedule_update_ha_state()

    @property
    def unique_id(self):
        """Return the button UUID."""
        return self._nhc2button.uuid

    @property
    def uuid(self):
        """Return the button UUID."""
        return self._nhc2button.uuid

    @property
    def should_poll(self):
        """Return false, since the button will push state."""
        return False

    @property
    def name(self):
        """Return the button name."""
        return self._nhc2button.name

    @property
    def available(self):
        """Return true if the button is online."""
        return self._nhc2button.online

    @property
    def is_on(self):
        """Return true if the button is on."""
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
            'model': BUTTON,
            'via_hub': (DOMAIN, self._nhc2button.profile_creation_id),
        }
