import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_HOSTNAME, CONF_PORT, CONF_REFRESHRATE, CONF_UNLOCKTIME, CONF_LOCKTIME, DEFAULT_PORT

class InfiniasConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @callback
    def async_get_options_flow(config_entry):
        return InfiniasOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("name"): str,
                    vol.Required(CONF_HOSTNAME): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                    vol.Optional(CONF_REFRESHRATE): int,
                    vol.Optional(CONF_UNLOCKTIME): int,
                    vol.Optional(CONF_LOCKTIME): int,
                }),
            )
        return self.async_create_entry(title=user_input["name"], data=user_input)
