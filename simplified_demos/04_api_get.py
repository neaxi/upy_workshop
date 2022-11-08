import urequests
import time


URL = "http://my-json-server.typicode.com/neaxi/upy_workshop/posts/{device}"


def api_get(url):
    """perform GET request on provided URL
    print request status (code + text)
    print raw data response
    return requests session object
    """
    resp = urequests.get(url)
    print("API GET status:", str(resp.status_code), resp.reason.decode())

    # try to extract "key" from API response
    print("Response - raw data:", resp.text)
    if "key" in resp.json().keys():
        key = resp.json()["key"]
        print("Response - extract from JSON:", key)
    return resp

def test_api_get():
    webaddress = URL.format(device="device00")
    session = api_get(webaddress)
    session.close()
    
    
test_api_get()
