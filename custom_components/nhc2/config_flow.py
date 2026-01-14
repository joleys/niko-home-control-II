"""Config flow to configure component."""
import socket
from typing import Any, Mapping
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_PORT
from .nhccoco.coco_login_validation import CoCoLoginValidation
from.hobbytoken import HobbyToken
from .const import (
    DOMAIN,
    DEFAULT_USERNAME,
    DEFAULT_PORT,
    CONF_ENABLE_STATISTICS,
    CONF_IMPORT_HISTORICAL_STATISTICS,
    CONF_HISTORICAL_STATISTICS_IMPORTED,
)

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

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Init NHC2FlowHandler."""
        self._errors = {}
        self._host = None
        self._password = None

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return Nhc2OptionsFlowHandler(config_entry)

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

        # Determine host from stored state (normal path) or fall back to user_input when provided
        host = self._host or user_input.get(CONF_HOST)
        if host is None:
            self._errors["base"] = "no_controller_found"
            return await self._show_host_config_form()

        # Make sure the controller is not already configured
        matches = list(
            filter(
                lambda x: x.data.get(CONF_HOST) == host,
                self.hass.config_entries.async_entries(DOMAIN),
            )
        )
        if len(matches) > 0:
            return self.async_abort(reason="single_instance_allowed")

        self._host = host
        password = user_input[CONF_PASSWORD]

        if not HobbyToken(password).is_a_token():
            self._errors["base"] = ("password_not_a_token")
            return await self._show_user_config_form()
    
        validator = CoCoLoginValidation(host, DEFAULT_USERNAME, password, DEFAULT_PORT)
        check = await validator.check_connection()
        if check > 0:
            self._errors["base"] = ("login_check_fail_%d" % check)
            return await self._show_user_config_form()

        # Store password for statistics options step
        self._password = password
        return await self.async_step_statistics_options()

    async def async_step_statistics_options(self, user_input=None):
        """Handle statistics configuration."""
        if user_input is not None:
            # Create entry with all configuration
            return self.async_create_entry(
                title=DEFAULT_USERNAME + ' (' + self._host + ')',
                data={
                    CONF_HOST: self._host,
                    CONF_PORT: DEFAULT_PORT,
                    CONF_USERNAME: DEFAULT_USERNAME,
                    CONF_PASSWORD: self._password
                },
                options={
                    CONF_ENABLE_STATISTICS: user_input.get(CONF_ENABLE_STATISTICS, False),
                    CONF_IMPORT_HISTORICAL_STATISTICS: user_input.get(CONF_IMPORT_HISTORICAL_STATISTICS, False),
                    CONF_HISTORICAL_STATISTICS_IMPORTED: False,
                }
            )

        return self.async_show_form(
            step_id="statistics_options",
            data_schema=vol.Schema({
                vol.Optional(CONF_ENABLE_STATISTICS, default=False): bool,
                vol.Optional(CONF_IMPORT_HISTORICAL_STATISTICS, default=False): bool,
            }),
            description_placeholders={
                "host": self._host
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


class Nhc2OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for NHC2."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Preserve existing historical import settings
            # (historical import is only configurable during initial setup)
            preserved_options = {
                CONF_IMPORT_HISTORICAL_STATISTICS: self._config_entry.options.get(CONF_IMPORT_HISTORICAL_STATISTICS, False),
                CONF_HISTORICAL_STATISTICS_IMPORTED: self._config_entry.options.get(CONF_HISTORICAL_STATISTICS_IMPORTED, False),
            }
            # Merge user input with preserved options
            return self.async_create_entry(title="", data={**preserved_options, **user_input})

        # Get current option
        current_enable = self._config_entry.options.get(CONF_ENABLE_STATISTICS, False)

        # Only show energy measurements toggle
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(CONF_ENABLE_STATISTICS, default=current_enable): bool,
            })
        )
