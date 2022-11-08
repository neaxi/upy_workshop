import urequests
import time


TOKEN = "Hello"
URL = "http://fra1.blynk.cloud/external/api/update?token=%s&V{stream}={value}" % TOKEN


def refresh_blynk(url):
    #resp = urequests.put(url, data=json.dumps(payload), headers=headers)
    resp = urequests.get(url)
    print("request status:", str(resp.status_code), str(resp.reason))
    print("Response - raw data:", resp.text)
    return resp


def test_api_upload():
    stream_id = "1"
    value = 5
    target = URL.format(stream=stream_id, value=value)
    session = refresh_blynk(target)
    session.close()

test_api_upload()
