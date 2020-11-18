"""Config flow to configure component."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, \
    CONF_PASSWORD
from nhc2_coco.coco_discover_profiles import CoCoDiscoverProfiles

from .const import DOMAIN, CONF_SWITCHES_AS_LIGHTS, DEFAULT_PORT


_LOGGER = logging.getLogger(__name__)
@config_entries.HANDLERS.register(DOMAIN)
class Nhc2FlowHandler(config_entries.ConfigFlow):
    """Config flow for NHC2 platform."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Init NHC2FlowHandler."""
        self._errors = {}
        self._all_cocos = []
        self._selected_coco = None

    async def async_step_import(self, user_input):
        """Import a config entry."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(
            title="configuration.yaml", data=user_input
        )

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            if CONF_USERNAME in user_input and \
                    self._selected_coco[1].replace(':', '') not in \
                    self.hass.config_entries.async_entries(DOMAIN):
                _LOGGER.debug(user_input)
                return self.async_create_entry(
                    title=self._selected_coco[1].replace(':', ''),
                    data={
                        CONF_HOST: self._selected_coco[0] if self._selected_coco[3] is None else self._selected_coco[3],
                        CONF_USERNAME: user_input[CONF_USERNAME],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                        CONF_SWITCHES_AS_LIGHTS: user_input[CONF_SWITCHES_AS_LIGHTS]
                    }
                )

            self._errors[CONF_USERNAME] = 'name_exists'

        disc = CoCoDiscoverProfiles()

        self._all_cocos = await disc.get_all_profiles()
        if self._all_cocos is None or len(self._all_cocos) == 0:
            return self.async_abort(reason="no_controller_found")

        return await self._show_host_config_form(
            self._all_cocos)

    async def async_step_host(self, user_input=None):
        #
        # users
        # for profile in self.all_cocos:
        #     profile[0]

        self._selected_coco = list(filter(lambda x: x[0] == user_input[CONF_HOST], self._all_cocos))[0]
        return await self._show_user_config_form(self._selected_coco)

    async def _show_host_config_form(self, all_cocos):
        """Show the configuration form to edit NHC2 data."""
        host_listing = {}
        first = None
        for i, x in enumerate(all_cocos):
            dkey = x[0] if x[3] is None else x[3]
            host_listing[dkey] = [x[3] + ' ('+x[0]+')']
            if i == 0:
                first = dkey
        return self.async_show_form(
            step_id='host',
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default=first): vol.In(host_listing)
            }),
            errors=self._errors,
        )

    async def _show_user_config_form(self, selected_coco=None):
        """Show the configuration form to edit NHC2 data."""
        profile_listing = {}
        profiles = selected_coco[2]
        first = None
        for i, x in enumerate(profiles):
            dkey = x.get('Uuid')
            profile_listing[dkey] = x.get('Name') + ' ('+x.get('Uuid')+')'
            if i == 0:
                first = dkey
        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME, default=first): vol.In(profile_listing),
                vol.Required(CONF_PASSWORD, default=None): str,
                vol.Optional(CONF_SWITCHES_AS_LIGHTS, default=False): bool
            }),
            errors=self._errors,
        )
