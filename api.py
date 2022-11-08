# connects to the WiFi network and sync time via NTP
import urequests
import time
import json


TOKEN = ""


# ----------------------------------------
# setup - headers, etc...
# if needed
# ----------------------------------------

headers = {}


# ----------------------------------------
# HTTP GET
# ----------------------------------------


def api_get(url):
    """perform GET request on provided URL
    print request status (code + text)
    print raw data response
    return requests session object
    """
    resp = urequests.get(url)
    print("API GET status:", str(resp.status_code), resp.reason)

    # try to extract "key" from API response
    print("Response - raw data:", resp.text)
    if "key" in resp.json().keys():
        key = resp.json()["key"]
        print("Response - extract from JSON:", key)
    return resp


def test_api_get():
    webaddress = "http://my-json-server.typicode.com/neaxi/upy_workshop/posts/device00"
    session = api_get(webaddress)
    session.close()


# ----------------------------------------
# HTTPS PUT
# ----------------------------------------


def api_put(url, payload):
    resp = urequests.put(url, data=json.dumps(payload), headers=headers)
    print("request status:", str(resp.status_code), str(resp.reason))
    print("Response - raw data:", resp.text)
    return resp


def test_api_put():
    stream_name = "numeric"
    target = (
        "https://api-m2x.att.com/v2/devices/{device_id}/streams/{stream}/value".format(
            device_id=m2x_device_id, stream=stream_name
        )
    )
    data = {"value": 5}

    session = api_put(target, data)
    session.close()
