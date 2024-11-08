from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    doors = await hass.async_add_executor_job(api.get_door_names)
    
    entities = []
    for door in doors:
        door_id = door["ActualValue"]
        friendly_name = door["FriendlyValue"]
        entities.append(InfiniasDoorSwitch(api, door_id, friendly_name))

    async_add_entities(entities, True)

class InfiniasDoorSwitch(SwitchEntity):
    def __init__(self, api, door_id, name):
        self.api = api
        self.door_id = door_id
        self._name = name
        self._is_locked = None

    @property
    def name(self):
        return f"{self._name} Door Lock"

    @property
    def is_on(self):
        """Return True if the door is unlocked."""
        return not self._is_locked

    async def async_turn_on(self, **kwargs):
        """Unlock the door."""
        await self.hass.async_add_executor_job(self.api.unlock_door, self.door_id)
        self._is_locked = False
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Lock the door."""
        await self.hass.async_add_executor_job(self.api.lock_door, self.door_id)
        self._is_locked = True
        self.async_write_ha_state()

    async def async_update(self):
        """Fetch the latest door status and update the switch."""
        door_status = await self.hass.async_add_executor_job(self.api.get_door_status, self.door_id)
        self._is_locked = door_status["IsLocked"]
