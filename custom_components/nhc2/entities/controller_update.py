from homeassistant.components.update import UpdateEntity, UpdateEntityFeature

from ..const import DOMAIN, BRAND

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2ControllerUpdateEntity(UpdateEntity):
    _attr_has_entity_name = True

    def __init__(self, hub, gateway):
        """Initialize a update."""
        self._hub = hub
        self._gateway = gateway

        self._attr_available = True
        self._attr_unique_id = 'latest_controller_config'
        self._attr_should_poll = False
        self._attr_auto_update = True
        self._attr_title = 'Controller Config'
        self._attr_supported_features = UpdateEntityFeature.INSTALL

    @property
    def name(self) -> str:
        return 'Latest Controller Config loaded'

    @property
    def device_info(self):
        return {
            'identifiers': {
                (DOMAIN, self._hub[1])
            },
        }

    @property
    def installed_version(self) -> str | None:
        return 'Up to date'

    @property
    def latest_version(self) -> str | None:
        return None

    @property
    def release_summary(self) -> str | None:
        if self.installed_version == self.latest_version:
            return None

        return 'Your Connected Controller has an update, to be able to use the latest configuration Home Assistant should be restarted.'

    async def async_install(self, version: str, backup: bool, **kwargs) -> None:
        _LOGGER.debug('Restarting Home Assistant')
        self.hass.async_create_task(self.hass.services.call('homeassistant', 'restart'))
