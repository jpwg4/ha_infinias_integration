async def async_setup_entry(hass, config_entry):
    hostname = config_entry.data["hostname"]
    port = config_entry.data["port"]
    username = config_entry.data["username"]
    password = config_entry.data["password"]

    # Initialize the API with parameters
    api = InfiniasAPI(hostname, port, username, password)

    # Store the API instance in hass.data for access by other parts of the integration
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = api

    # Do any additional setup here
    return True
