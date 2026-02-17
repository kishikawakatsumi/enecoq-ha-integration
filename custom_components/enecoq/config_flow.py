from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries

from .const import (
    DOMAIN,
    CONF_TODAY_PATH, CONF_MONTH_PATH,
    CONF_SCAN_INTERVAL, CONF_STALE_MINUTES,
    DEFAULT_TODAY_PATH, DEFAULT_MONTH_PATH,
    DEFAULT_SCAN_INTERVAL, DEFAULT_STALE_MINUTES,
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="enecoQ",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Optional(CONF_TODAY_PATH, default=DEFAULT_TODAY_PATH): str,
                vol.Optional(CONF_MONTH_PATH, default=DEFAULT_MONTH_PATH): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.Coerce(int),
                vol.Optional(CONF_STALE_MINUTES, default=DEFAULT_STALE_MINUTES): vol.Coerce(int),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)
