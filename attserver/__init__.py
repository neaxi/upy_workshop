try:
    import requests
except ImportError:
    import lib.urequests as requests

import json

try:
    import datetime

    F_DT = True
except ImportError:
    F_DT = False

try:
    import ulogging as logging
except ImportError:
    import logging

try:
    from . import conf
except ImportError:
    import conf

BASE_URL = conf.URL
HDR_JSON = conf.HDR_JSON

FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger()


def gen_headers(token: str = None):
    headers = conf.HDR_JSON
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def wrap_connection(
    func, url, headers=gen_headers(), payload=None, timeout=conf.TIMEOUT
):
    """wrapper for HTTP calls, to have them retry the connection on exception (timeout, reachability, etc..)"""
    for i in range(conf.RETRY_ATTEMPTS):
        try:
            return func(url, headers=headers, data=payload, timeout=timeout)
        except BaseException as exc:
            logger.warning(f"Connection failed - {exc}. Retrying...")


def parse_resp(resp: requests.Response) -> tuple:
    """get response from the request and add status_code to it"""
    if not resp.text:
        return (resp.status_code, "")
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        data = resp.text
    return (resp.status_code, data, resp)


def get_master_token(usr: str = None, pwd: str = None) -> tuple:
    """
    curl -X POST \
    --header "Content-Type: application/json" \
    --data '{"email": "$mail", "password": "$pwd"}' \
    $URL
    """
    if not usr or not pwd:
        raise ValueError("Credentials not provided")
    payload = json.dumps({"email": usr, "password": pwd})
    resp = wrap_connection(requests.post, f"{BASE_URL}/master-token", payload=payload)
    return parse_resp(resp)


def get_all_devices(master_token: str) -> tuple:
    """
    curl -X GET \
    --header "Authorization: Bearer $master_token" \
    $URL
    """
    resp = wrap_connection(
        requests.get, f"{BASE_URL}/devices", headers=gen_headers(master_token)
    )
    return parse_resp(resp)


def register_device(dev_name: str = None) -> tuple:
    """
    curl -X POST \
    --header "Content-Type: application/json" \
    --data '{"name": "$dev_name"}' \
    $URL
    """
    payload = json.dumps({"name": dev_name})
    resp = wrap_connection(requests.post, f"{BASE_URL}/devices", payload=payload)
    return parse_resp(resp)


def get_device(dev_name: str, token: str) -> tuple:
    resp = wrap_connection(
        requests.get, f"{BASE_URL}/devices/{dev_name}", headers=gen_headers(token)
    )
    return parse_resp(resp)


def get_device_data(dev_name: str, token: str) -> tuple:
    """ 
    curl -X GET \
    --header "Authorization: Bearer $token" \
    --$URL/devices/$DEV/datapoints
    """
    resp = wrap_connection(
        requests.get,
        f"{BASE_URL}/devices/{dev_name}/datapoints",
        headers=gen_headers(token),
    )
    return parse_resp(resp)


def post_device_data(dev_name: str, token: str, value: int) -> tuple:
    payload = json.dumps({"value": value})
    resp = wrap_connection(
        requests.post,
        f"{BASE_URL}/devices/{dev_name}/datapoints",
        payload=payload,
        headers=gen_headers(token),
    )
    return parse_resp(resp)


def print_data_series(data: list) -> list:
    """gets output from /datapoints"""
    out = []
    for datapoint in data:
        if not isinstance(datapoint, dict):
            print(f"Fishy datapoint - {datapoint}")
        try:
            if F_DT:
                date = datetime.datetime.fromisoformat(datapoint["updated_at"])
                date = date.strftime("%Y-%m-%d %H:%M:%S")
                out.append(f"{date},{datapoint['value']}")
            else:
                out.append(datapoint["value"])
        except KeyError:
            logger.warning(datapoint)
    return out[::-1]


def delete_device(dev_name: str, token: str) -> tuple:
    """
    curl -X DELETE \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer NDMxx8rW" \
    https://iot-workshop-api.up.railway.app/devices/01GPE2E...
    """
    resp = wrap_connection(
        requests.delete, f"{BASE_URL}/devices/{dev_name}", headers=gen_headers(token)
    )
    return parse_resp(resp)


def delete_all_devices(master_token: str):
    devices = get_all_devices(master_token)
    for dev_id in [device["id"] for device in devices[1]]:
        delete_device(dev_id, master_token)
