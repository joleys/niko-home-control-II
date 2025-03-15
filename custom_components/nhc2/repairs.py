import voluptuous as vol

from homeassistant import data_entry_flow
from homeassistant.components.repairs import RepairsFlow
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_PORT
from homeassistant.core import HomeAssistant
from .const import DEFAULT_USERNAME, DEFAULT_PORT
from .nhccoco.coco_login_validation import CoCoLoginValidation
from.hobbytoken import HobbyToken

import logging

_LOGGER = logging.getLogger(__name__)


REAUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME, default=DEFAULT_USERNAME): vol.In([DEFAULT_USERNAME]), # username isn't actually editable
        vol.Required(CONF_PASSWORD): str,
    }
)

class NotAuthorisedRepairFlow(RepairsFlow):
    async def async_step_init(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult:
        return await (self.async_step_confirm())

    async def async_step_confirm(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult:
        config_entry = self.data['entry']
        errors = {}

        if user_input is not None:
            data = config_entry.data.copy()
            data[CONF_PASSWORD] = user_input[CONF_PASSWORD]

            if not HobbyToken(data[CONF_PASSWORD]).is_a_token():
                errors[CONF_PASSWORD] = ("password_not_a_token")
            else:
                validator = CoCoLoginValidation(data[CONF_HOST], data[CONF_USERNAME], data[CONF_PASSWORD], data[CONF_PORT])
                check = await validator.check_connection()
                if check > 0:
                    _LOGGER.error("Authentication failed: %d", check)
                    errors["base"] = ("login_check_fail_%d" % check)
                else:
                    self.hass.config_entries.async_update_entry(config_entry, data=data)
                    await self.hass.config_entries.async_reload(config_entry.entry_id)
                    return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="confirm",
            description_placeholders={
                "host": config_entry.data[CONF_HOST],
                "expiration": HobbyToken(config_entry.data[CONF_PASSWORD]).get_expiration_date().strftime("%d/%m/%y")
            },
            errors=errors,
            data_schema=REAUTH_SCHEMA
        )

class MigrateToTokenAuthRepairFlow(RepairsFlow):
    async def async_step_init(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult:
        return await (self.async_step_confirm())

    async def async_step_confirm(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult:
        config_entry = self.data['entry']
        errors = {}

        if user_input is not None:
            data = config_entry.data.copy()
            data[CONF_USERNAME] = DEFAULT_USERNAME
            data[CONF_PORT] = DEFAULT_PORT
            data[CONF_PASSWORD] = user_input[CONF_PASSWORD]

            if not HobbyToken(data[CONF_PASSWORD]).is_a_token():
                errors[CONF_PASSWORD] = ("password_not_a_token")
            else:
                validator = CoCoLoginValidation(data[CONF_HOST], data[CONF_USERNAME], data[CONF_PASSWORD], data[CONF_PORT])
                check = await validator.check_connection()
                if check > 0:
                    _LOGGER.error("Authentication failed: %d", check)
                    errors["base"] = ("login_check_fail_%d" % check)
                else:
                    self.hass.config_entries.async_update_entry(config_entry, data=data)
                    await self.hass.config_entries.async_reload(config_entry.entry_id)
                    return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="confirm",
            description_placeholders={
                "host": config_entry.data[CONF_HOST]
            },
            errors=errors,
            data_schema=REAUTH_SCHEMA
        )

async def async_create_fix_flow(
        hass: HomeAssistant,
        issue_id: str,
        data: dict[str, str | int | float | None] | None,
) -> RepairsFlow:
    if issue_id == "not_authorised" or issue_id == "token_about_to_expire":
        return NotAuthorisedRepairFlow()
    if issue_id == "migrate_to_token_auth":
        return MigrateToTokenAuthRepairFlow()