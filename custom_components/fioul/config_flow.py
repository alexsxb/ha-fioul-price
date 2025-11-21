from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, DEFAULT_POLLRATE, CONF_POLLRATE


class FioulConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fioul."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            pollrate = user_input.get(CONF_POLLRATE, DEFAULT_POLLRATE)
            try:
                pollrate = int(pollrate)
            except (TypeError, ValueError):
                pollrate = 0

            if pollrate < 1 or pollrate > 24:
                errors[CONF_POLLRATE] = "invalid_pollrate"
            else:
                # Nur eine Instanz erlauben
                if self._async_current_entries():
                    return self.async_abort(reason="single_instance_allowed")

                return self.async_create_entry(
                    title="Fioul Price",
                    data={CONF_POLLRATE: pollrate},
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_POLLRATE, default=DEFAULT_POLLRATE): int,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
