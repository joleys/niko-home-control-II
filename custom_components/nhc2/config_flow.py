"""Config flow to configure component."""
import socket
from typing import Any, Mapping
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_PORT
from .nhccoco.coco_login_validation import CoCoLoginValidation
from.hobbytoken import HobbyToken
from .const import DOMAIN, DEFAULT_USERNAME, DEFAULT_PORT

import logging

_LOGGER = logging.getLogger(__name__)


REAUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME, default=DEFAULT_USERNAME): vol.In([DEFAULT_USERNAME]), # username isn't actually editable
        vol.Required(CONF_PASSWORD): str,
    }
)

@config_entries.HANDLERS.register(DOMAIN)
class Nhc2FlowHandler(config_entries.ConfigFlow):
    """Config flow for NHC2 platform."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Init NHC2FlowHandler."""
        self._errors = {}
        self._host = None

    async def async_step_import(self, user_input):
        """Import a config entry."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(
            title="configuration.yaml", data=user_input
        )

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is None:
            return await self._show_host_config_form()

        self._errors = {}

        # Make sure the controller is not already configured
        matches = list(filter(lambda x: ((x.data[CONF_HOST] == user_input[CONF_HOST])),
                                self.hass.config_entries.async_entries(DOMAIN)))
        if len(matches) > 0:
            return self.async_abort(reason="single_instance_allowed")

        host = self._host
        password = user_input[CONF_PASSWORD]

        if not HobbyToken(password).is_a_token():
            self._errors["base"] = ("password_not_a_token")
            return await self._show_user_config_form(user_input)
    
        validator = CoCoLoginValidation(host, DEFAULT_USERNAME, password, DEFAULT_PORT)
        check = await validator.check_connection()
        if check > 0:
            self._errors["base"] = ("login_check_fail_%d" % check)
            return await self._show_user_config_form(user_input)

        return self.async_create_entry(
            title=DEFAULT_USERNAME + ' (' + host + ')',
            data={
                CONF_HOST: host,
                CONF_PORT: DEFAULT_PORT,
                CONF_USERNAME: DEFAULT_USERNAME,
                CONF_PASSWORD: password
            }
        )

    async def _show_host_config_form(self):
        """Show the form to manually enter an IP / hostname."""
        return self.async_show_form(
            step_id='host',
            errors=self._errors,
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default=None): str
            })
        )

    async def async_step_host(self, user_input=None):
        if user_input is None:
            return True

        self._errors = {}
        try:
            host = socket.gethostbyaddr(user_input[CONF_HOST])[0]
        except Exception as e:
            host = None

        if host is None:
            return self.async_abort(reason="no_controller_found")

        self._host = user_input[CONF_HOST]
        return await self._show_user_config_form()

    async def _show_user_config_form(self):
        """Show form to enter the credentials."""
        errors: dict[str, str] = {}
        return self.async_show_form(
            step_id='user',
            errors=errors,
            description_placeholders={
                "host": self._host
            },
            data_schema=REAUTH_SCHEMA
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        errors = {}
        config_entry = self._get_reconfigure_entry()
        self._host = config_entry.data[CONF_HOST]

        if user_input is not None:
            if not HobbyToken(user_input[CONF_PASSWORD]).is_a_token():
                errors[CONF_PASSWORD] = ("password_not_a_token")
            else:
                validator = CoCoLoginValidation(config_entry.data[CONF_HOST], DEFAULT_USERNAME, user_input[CONF_PASSWORD], DEFAULT_PORT)
                check = await validator.check_connection()
                if check > 0:
                    errors["base"] = ("login_check_fail_%d" % check)
                else:
                    return self.async_update_reload_and_abort(
                        self._get_reconfigure_entry(),
                        data_updates={CONF_PASSWORD: user_input[CONF_PASSWORD]},
                    )

        if config_entry.data[CONF_USERNAME] == DEFAULT_USERNAME:
            return self.async_show_form(
                step_id="reconfigure",
                errors=errors,
                description_placeholders={
                    "host": config_entry.data[CONF_HOST],
                    "expiration": HobbyToken(config_entry.data[CONF_PASSWORD]).get_expiration_date().strftime("%d/%m/%y")
                },
                data_schema=REAUTH_SCHEMA
            )
        else:
            return self.async_show_form(
                step_id="reconfigure_use_token",
                errors=errors,
                description_placeholders={
                    "host": config_entry.data[CONF_HOST]
                },
                data_schema=REAUTH_SCHEMA
            )
