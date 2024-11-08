from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    doors = await hass.async_add_executor_job(api.get_door_names)

    sensors = []
    for door in doors:
        door_id = door["ActualValue"]
        friendly_name = door["FriendlyValue"]
        door_status = await hass.async_add_executor_job(api.get_door_status, door_id)

        sensors.append(InfiniasDoorStatusSensor(api, door_id, friendly_name, door_status))
    
    async_add_entities(sensors, True)

class InfiniasDoorStatusSensor(BinarySensorEntity):
    def __init__(self, api, door_id, name, door_status):
        self.api = api
        self.door_id = door_id
        self._name = name
        self._state = None
        self.update_door_status(door_status)

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state in ["UnlockedOpen", "UnlockedClosed"]

    def update_door_status(self, status):
        is_locked = status["IsLocked"]
        is_open = status["IsOpen"]
        service_overridden = status["ServiceOverridden"]

        if is_locked:
            self._state = "LockedClosed" if not is_open else "LockedOpen"
        else:
            self._state = "UnlockedClosed" if not is_open else "UnlockedOpen"

        # Handle icons, colors, and additional attributes here.

    async def async_update(self):
        door_status = await self.hass.async_add_executor_job(self.api.get_door_status, self.door_id)
        self.update_door_status(door_status)
