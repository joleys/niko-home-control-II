from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory

from .helpers import camel_case_to_words

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.device import CoCoDevice


class Nhc2BooleanHasStatusTrueCanControlFalseEntity(BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, property_name, device_instance: CoCoDevice, hub, gateway, is_diagnostic: bool = False):
        """Initialize a binary sensor."""
        self._original_property_name = property_name
        self._property_name_with_underscores = '_'.join(camel_case_to_words(property_name)).lower()
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_' + self._property_name_with_underscores
        self._attr_should_poll = False

        self._attr_state = getattr(self._device, self._property_name_with_underscores) is True
        self._attr_state_class = None

        if is_diagnostic:
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return ' '.join(camel_case_to_words(self._original_property_name))

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': BRAND,
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def is_on(self) -> bool:
        return getattr(self._device, self._property_name_with_underscores) is True

    def on_change(self):
        self.schedule_update_ha_state()
