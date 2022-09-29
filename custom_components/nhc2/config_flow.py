"""Config flow to configure component."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, \
    CONF_PASSWORD, CONF_ADDRESS, CONF_PORT
from .coco_discover_profiles import CoCoDiscoverProfiles
from .coco_login_validation import CoCoLoginValidation

from .const import DOMAIN, CONF_SWITCHES_AS_LIGHTS, KEY_MANUAL

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class Nhc2FlowHandler(config_entries.ConfigFlow):
    """Config flow for NHC2 platform."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Init NHC2FlowHandler."""
        self._all_cocos = []
        self._selected_coco = None
        self._errors = {}

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
            # TODO We might want to check this before showing dialogs in the future
            matches = list(filter(lambda x: ((x.data[CONF_ADDRESS] == self._selected_coco[1]) and (
                    x.data[CONF_USERNAME] == user_input[CONF_USERNAME])),
                                  self.hass.config_entries.async_entries(DOMAIN)))

            if len(matches) > 0:
                return self.async_abort(reason="single_instance_allowed")

            user_name = list(filter(lambda x: (x.get('Uuid') == user_input[CONF_USERNAME]), self._selected_coco[2]))[
                0].get('Name')
            host = self._selected_coco[0] if self._selected_coco[3] is None else self._selected_coco[3]
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            port = 8884 if user_input[CONF_USERNAME] == 'hobby' else 8883
            validator = CoCoLoginValidation(host, username, password, port)
            check = await validator.check_connection()

            if check > 0:
                self._errors["base"] = ("login_check_fail_%d" % check)
                return await self._show_user_config_form()

            return self.async_create_entry(
                title=user_name + ' (' + host + ')',
                data={
                    CONF_HOST: host,
                    CONF_ADDRESS: self._selected_coco[1],
                    CONF_PORT: port,
                    CONF_USERNAME: username,
                    CONF_PASSWORD: password,
                    CONF_SWITCHES_AS_LIGHTS: user_input[CONF_SWITCHES_AS_LIGHTS]
                }
            )

        disc = CoCoDiscoverProfiles()

        self._all_cocos = await disc.get_all_profiles()
        for coco in self._all_cocos:
            if coco[2] is not None:
                coco[2].insert(0, {
                    'Uuid': 'hobby',
                    'Name': 'hobby',
                    'Type': 'hobby'
                })

        return await self._show_host_config_form()

    async def async_step_host(self, user_input=None):
        self._errors = {}
        if user_input[CONF_HOST] == KEY_MANUAL:
            return await self._show_manual_host_config_form()
        else:
            self._selected_coco = \
                list(filter(lambda x: x[0] == user_input[CONF_HOST] or x[3] == user_input[CONF_HOST], self._all_cocos))[0]
        return await self._show_user_config_form()

    async def async_step_manual_host(self, user_input=None):
        self._errors = {}

        disc = CoCoDiscoverProfiles(user_input[CONF_HOST])
        self._all_cocos = await disc.get_all_profiles()
        if self._all_cocos is not None and len(self._all_cocos) == 1:
            self._selected_coco = self._all_cocos[0]
            _LOGGER.debug(str(self._all_cocos))
            for coco in self._all_cocos:
                if coco[2] is not None:
                    coco[2].insert(0, {
                        'Uuid': 'hobby',
                        'Name': 'hobby',
                        'Type': 'hobby'
                    })

            return await self._show_user_config_form()
        else:
            return self.async_abort(reason="no_controller_found")

    async def _show_host_config_form(self):
        """Show the configuration form to edit NHC2 data."""
        host_listing = {}
        first = None
        for i, x in enumerate(self._all_cocos):
            dkey = x[0] if x[3] is None else x[3]
            host_listing[dkey] = [x[3] + ' (' + x[0] + ')']
            if i == 0:
                first = dkey
        host_listing[KEY_MANUAL] = 'Manual Input'
        if first is None:
            first = KEY_MANUAL
        return self.async_show_form(
            step_id='host',
            errors=self._errors,
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default=first): vol.In(host_listing)
            }),
        )

    async def _show_user_config_form(self):
        """Show the configuration form to edit NHC2 data."""
        profile_listing = {}
        profiles = self._selected_coco[2]
        first = None
        for i, x in enumerate(profiles):
            dkey = x.get('Uuid')
            profile_listing[dkey] = x.get('Name')
            if i == 0:
                first = dkey
        return self.async_show_form(
            step_id='user',
            errors=self._errors,
            description_placeholders={
                "host": self._selected_coco[3] if self._selected_coco[3] is not None else self._selected_coco[0]
            },
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME, default=first): vol.In(profile_listing),
                vol.Required(CONF_PASSWORD, default=None): str,
                vol.Optional(CONF_SWITCHES_AS_LIGHTS, default=False): bool
            }),
        )

    async def _show_manual_host_config_form(self):
        """Show the configuration form to edit NHC2 data."""
        return self.async_show_form(
            step_id='manual_host',
            errors=self._errors,
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default=None): str
            }),
        )
