from random import randint
import time

try:
    import ulogging as logging
except ImportError:
    import logging

try:
    import attserver
except ImportError:
    import __init__ as attserver

FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger()


def test1(usr=None, pwd=None):
    """get master token
    use it to fetch all devices"""
    logger.info("Fetching master token using provided creds.")
    master = attserver.get_master_token(usr=usr, pwd=pwd)
    logger.debug(master)
    master_token = master[1]["token"]

    logger.info("Fetching list of all devices")
    devices = attserver.get_all_devices(master_token)
    logger.debug(devices)


def test2():
    """
    - register new device
    - fetch it via GET
    - update values via multiple POST
    - fetch all values
    - DELETE device
    """
    logger.info("Registering device")
    device = attserver.register_device("TEST_FS_DEVICE")
    if device[0] == 200:
        device = device[1]
    else:
        logger.error("Device creation failed")
        logger.error(device)
        raise ValueError()

    logger.debug(device)

    logger.info("Fetching device")
    device_data = attserver.get_device(device["id"], device["token"])
    logger.debug(device_data)

    logger.info("Log some data points")
    rand_data = [randint(0, 420) for i in range(20)]

    for i in [23, 42, 69, 420, 666] + rand_data:
        logger.debug(f"Sending value: {i}")
        update = attserver.post_device_data(device["id"], device["token"], i)
        if update[0] != 200:
            logger.error(f"Updating device with value '{i}' was not successful")
            logger.debug(f"{update[2].status_code} - {update[2].text}")
        time.sleep(1)

    logger.info("Fetching logged data")
    datapoints = attserver.get_device_data(device["id"], device["token"])
    logger.debug(datapoints)
    logger.debug(f"Readable datapoints: {attserver.print_data_series(datapoints[1])}")

    logger.info("Deleting device")
    attserver.delete_device(device["id"], device["token"])
    logger.info("Device deleted")

    logger.info("Confirming deletion")
    device_data = attserver.get_device(device["id"], device["token"])
    if device_data[0] != 404:
        logger.error("Deletion failed - verify it")
        logger.debug(f"{device_data[2].status_code} - {device_data[2].text}")
    logger.info("Done")


def test3():
    logger.info("Registering device")
    device = attserver.register_device("DEMO DEVICE")
    if device[0] == 200:
        device = device[1]
    else:
        logger.error("Device creation failed")
        logger.error(device)
        raise ValueError()

    logger.debug(device)

    logger.info("Log some data points")
    for i in range(0, 100):
        if i % 2 == 0:
            data = i
        else:
            data = 100 - i
        logger.debug(f"Sending value: {data}")
        update = attserver.post_device_data(device["id"], device["token"], data)
        if update[0] != 200:
            logger.error(f"Updating device with value '{i}' was not successful")
            logger.debug(f"{update[2].status_code} - {update[2].text}")
        # time.sleep(1)


if "__main__" in __name__:
    # test1("name", "password")
    # test2()
    # test3()
    ...
