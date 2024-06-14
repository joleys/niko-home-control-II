import voluptuous as vol

from homeassistant import data_entry_flow
from homeassistant.components.homeassistant import SERVICE_HOMEASSISTANT_RESTART
from homeassistant.components.repairs import RepairsFlow
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_PORT
from homeassistant.core import HomeAssistant

from .nhccoco.coco_login_validation import CoCoLoginValidation

import logging

_LOGGER = logging.getLogger(__name__)


class NotAuthorisedRepairFlow(RepairsFlow):
    def __init__(self):
        self._errors = {}

    async def async_step_init(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult:
        return await (self.async_step_confirm())

    async def async_step_confirm(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult:
        if user_input is not None:
            config_entry = self.data['entry']
            data = config_entry.data.copy()
            data[CONF_PASSWORD] = user_input[CONF_PASSWORD]

            validator = CoCoLoginValidation(data[CONF_HOST], data[CONF_USERNAME], data[CONF_PASSWORD], data[CONF_PORT])
            check = await validator.check_connection()

            if check > 0:
                _LOGGER.error("Authentication failed: %d", check)
                self._errors["base"] = ("login_check_fail_%d" % check)
            else:
                self.hass.config_entries.async_update_entry(config_entry, data=data)
                await self.hass.services.async_call(
                    "homeassistant",
                    SERVICE_HOMEASSISTANT_RESTART,
                )
                return self.async_create_entry(data={})

        return self.async_show_form(
            step_id="confirm",
            errors=self._errors,
            data_schema=vol.Schema({
                vol.Required(CONF_PASSWORD, default=None): str,
            })
        )


async def async_create_fix_flow(
        hass: HomeAssistant,
        issue_id: str,
        data: dict[str, str | int | float | None] | None,
) -> RepairsFlow:
    if issue_id == "not_authorised":
        return NotAuthorisedRepairFlow()
