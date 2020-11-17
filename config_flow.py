"""Config flow to configure component."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, \
    CONF_PASSWORD

from .const import DOMAIN, CONF_SWITCHES_AS_LIGHTS, DEFAULT_PORT


@config_entries.HANDLERS.register(DOMAIN)
class Nhc2FlowHandler(config_entries.ConfigFlow):
    """Config flow for NHC2 platform."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Init NHC2FlowHandler."""
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
            if user_input[CONF_USERNAME] not in \
                    self.hass.config_entries.async_entries(DOMAIN):
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )

            self._errors[CONF_USERNAME] = 'name_exists'

        # default location is set hass configuration
        return await self._show_config_form(
            host=None,
            port=DEFAULT_PORT,
            username=None,
            password=None,
            switches_as_lights=None)

    async def _show_config_form(self, host=None, port=None,
                                username=None,
                                password=None, switches_as_lights=None):
        """Show the configuration form to edit NHC2 data."""
        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default=host): str,
                vol.Optional(CONF_PORT, default=port): int,
                vol.Required(CONF_USERNAME, default=username): str,
                vol.Required(CONF_PASSWORD, default=password): str,
                vol.Optional(CONF_SWITCHES_AS_LIGHTS, default=switches_as_lights, description='All switches are lights'): bool
            }),
            errors=self._errors,
        )
