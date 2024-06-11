from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import STATE_ON

from ..nhccoco.devices.naso_smartplug import CocoNasoSmartplug
from .nhc_entity import NHCBaseEntity

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2NasoSmartplugReportInstantUsageEntity(NHCBaseEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoNasoSmartplug, hub, gateway):
        """Initialize a binary sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid + '_report_instant_usage'
        self._attr_state = self._device.is_report_instant_usage
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Report Instant Usage'

    @property
    def is_on(self) -> bool:
        return self._device.is_report_instant_usage

    def on_change(self):
        super().on_change()

        # Re-enable reporting when it is turned off
        if self._device.is_report_instant_usage is False and not self._is_report_instant_usage_re_enabling_disabled():
            self._device.enable_report_instant_usage(self._gateway)
            self.schedule_update_ha_state()

    def _is_report_instant_usage_re_enabling_disabled(self) -> bool:
        if not self._device.is_online:
            return True

        disable_report_instant_usage_re_enabling_entity = self.hass.states.get(
            self.entity_id.replace('binary_sensor.', 'switch.').replace('_report_instant_usage',
                                                                        '_disable_report_instant_usage_re_enabling')
        )

        if disable_report_instant_usage_re_enabling_entity is None:
            _LOGGER.warning(f'{self.name} no Disable Report Instant Usage Re-enabling entity found.')
            return False

        return disable_report_instant_usage_re_enabling_entity.state == STATE_ON
