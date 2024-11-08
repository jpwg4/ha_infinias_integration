class InfiniasAPI:
    def lock_door(self, door_id, duration=None):
        url = f"{self.base_url}/Doors"
        params = {"LockStatus": "Locked", "DoorIds": door_id, "Duration": duration or self.default_locktime}
        response = requests.put(url, params=params, auth=self.auth)
        response.raise_for_status()

    def unlock_door(self, door_id, duration=None):
        url = f"{self.base_url}/Doors"
        params = {"LockStatus": "Unlocked", "DoorIds": door_id, "Duration": duration or self.default_unlocktime}
        response = requests.put(url, params=params, auth=self.auth)
        response.raise_for_status()
