from homeassistant.components.input_boolean import RestoreEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import STATE_OFF, STATE_ON
import logging
_LOGGER = logging.getLogger(__name__)

class NHCBaseEntity():
    def __init__(self, device_instance, hub, gateway):
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)
        self._attr_state_class = None

    def on_change(self):
        if self.hass is None:
            # This is where we catch the ghost!
            _LOGGER.warning(
                "NHC2 Entity '%s' (UUID: %s) received an update but is not linked to Home Assistant. "
                "This usually happens if the device was removed or is still initializing.",
                self.name, 
                self._device.uuid
            )
            return
        self._attr_available = self._device.is_online
        self.schedule_update_ha_state()


class NHCDisableReportInstantUsageReEnablingEntity(NHCBaseEntity, RestoreEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance, hub, gateway):
        """Initialize an input boolean."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = self._device.uuid + '_disable_report_instant_usage_re_enabling'
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_available = True  # This entity doesn't depend on the device being online
        self._state = STATE_OFF

    @property
    def name(self) -> str:
        return 'Disable Report Instant Usage Re-enabling'

    @property
    def state(self):
        return self._state

    @property
    def is_on(self) -> bool:
        return self._state == STATE_ON

    def on_change(self):
        pass

    def _start_reporting_if_enabled(self):
        if not self.is_on:
            self._device.enable_report_instant_usage(self._gateway)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        self._state = STATE_ON if state and state.state == STATE_ON else STATE_OFF
        self.async_schedule_update_ha_state(True)
        self._start_reporting_if_enabled()

    async def async_turn_on(self, **kwargs):
        self._state = STATE_ON
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._state = STATE_OFF
        self._start_reporting_if_enabled()
        self.async_write_ha_state()
