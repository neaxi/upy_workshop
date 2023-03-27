import time

try:
    import ulogging as logging
except ImportError:
    import logging

import random

import attserver


FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger()

DELAY = 1

logger.info("Registering device")
device = attserver.register_device("TEST_ESP32_DEMO")
logger.debug(device)
if device[0] == 200:
    device = device[1]

while True:
    i = random.randint(0, 100)

    update = attserver.post_device_data(device["id"], device["token"], i)
    if update[0] == 200:
        logger.info(f"Server updated - {i}")
    else:
        logger.error(f"Updating device with value '{i}' was not successful")
        logger.debug(f"{update[2].status_code} - {update[2].text}")

    time.sleep(DELAY)
