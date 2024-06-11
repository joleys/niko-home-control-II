from datetime import datetime
from homeassistant.components.update import UpdateEntity, UpdateEntityFeature

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.controller import CocoController

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2ControllerLatestConfigLoadedUpdateEntity(UpdateEntity):
    """ The timestamp for the first and last time the devices.list is received are used as version information. """
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoController, hub, gateway):
        """Initialize a update."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = True
        self._attr_unique_id = 'controller_has_newer_config'
        self._attr_should_poll = False
        self._attr_auto_update = True
        self._attr_title = 'Controller Config'

    @property
    def name(self) -> str:
        return 'Latest Controller Config'

    @property
    def device_info(self):
        return {
            'identifiers': {
                (DOMAIN, self._hub[1])
            },
        }

    @property
    def installed_version(self) -> str | None:
        if self._device.first_time_device_list_received is None:
            return None

        return self._device.first_time_device_list_received.ctime()

    @property
    def latest_version(self) -> str | None:
        if self._device.last_time_device_list_received is None:
            return None

        return self._device.last_time_device_list_received.ctime()

    @property
    def release_summary(self) -> str | None:
        if self.installed_version == self.latest_version:
            return None

        return """Your Connected Controller has probably been updated with a new configuration. To continue 
        using the integration in Home Assistant, **please restart Home Assistant**."""

    def on_change(self):
        if self.hass is None:
            return

        self.schedule_update_ha_state()
