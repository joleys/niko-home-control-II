from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import STATE_ON

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.generic_smartplug import CocoGenericSmartplug

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2GenericSmartplugReportInstantUsageEntity(BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericSmartplug, hub, gateway):
        """Initialize a binary sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_report_instant_usage'
        self._attr_should_poll = False

        self._attr_state = self._device.is_report_instant_usage
        self._attr_state_class = None
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Report Instant Usage'

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
        return self._device.is_report_instant_usage

    def on_change(self):
        # Re-enable reporting when it is turned off
        if self._device.is_report_instant_usage is False:
            if self._is_report_instant_usage_re_enabling_disabled():
                _LOGGER.debug(f'{self.name} re-enabling disabled')
                return

            _LOGGER.debug(f'{self.name} re-enabled')
            self._device.enable_report_instant_usage(self._gateway)

        self.schedule_update_ha_state()

    def _is_report_instant_usage_re_enabling_disabled(self) -> bool:
        disable_report_instant_usage_re_enabling_entity = self.hass.states.get(
            self.entity_id.replace('binary_sensor.', 'switch.').replace('_report_instant_usage',
                                                                        '_disable_report_instant_usage_re_enabling')
        )

        if disable_report_instant_usage_re_enabling_entity is None:
            _LOGGER.debug(f'{self.name} no Disable Report Instant Usage Re-enabling entity found.')
            return False

        return disable_report_instant_usage_re_enabling_entity.state == STATE_ON
