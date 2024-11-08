import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class InfiniasConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        
        if user_input is not None:
            # Perform any input validation or initial setup here, if needed
            return self.async_create_entry(title=user_input["name"], data=user_input)

        # Add fields for hostname, port, username, password, refreshrate, defaultunlocktime, and defaultlocktime
        data_schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("hostname"): str,
            vol.Optional("port", default=18779): int,
            vol.Required("username"): str,
            vol.Required("password"): str,
            vol.Optional("refreshrate", default=10): int,
            vol.Optional("defaultunlocktime", default=5): int,
            vol.Optional("defaultlocktime", default=5): int,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
