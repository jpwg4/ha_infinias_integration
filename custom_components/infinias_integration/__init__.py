from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from .infinias_api import InfiniasAPI

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA Infinias Integration from a config entry."""
    hostname = entry.data["hostname"]
    port = entry.data.get("port")
    username = entry.data.get("username")
    password = entry.data.get("password")

    api = InfiniasAPI(hostname, port, username, password)

    # Store the API instance for later use
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"api": api}

    # Load entities and services
    await hass.config_entries.async_forward_entry_setups(entry, ["binary_sensor", "switch"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "binary_sensor")
    unload_ok = unload_ok and await hass.config_entries.async_forward_entry_unload(entry, "switch")

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
