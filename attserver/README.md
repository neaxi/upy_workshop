# attserver
Module for interfacing with local test server API

Module functoons:

```py
# register device to server
attserver.register_device(dev_id: str = None)

# get device details / confirm the device got created
attserver.get_device(dev_id: str, token: str)

# send new datapoint 
attserver.post_device_data(dev_id: str, token: str, value: int)

# get all datapoints associated with the device
attserver.get_device_data(dev_id: str, token: str)

# parses datapoints from get_device_data response 
attserver.print_data_series(data: list)

# removes device from the server
attserver.delete_device(dev_id: str, token: str) -> tuple:



# obtain access token with elevated privileges
attserver.get_master_token(usr: str = None, pwd: str = None) 

# get info about all devices 
attserver.get_all_devices(master_token: str)

# remove all devices from the server
attserver.delete_all_devices(master_token: str)
```