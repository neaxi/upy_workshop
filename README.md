# MicroPython workshop on ESP32 
These informations are not intended as a stand alone study material but rather as an aid and possible future reference for students which attended the workshop in person.
## Set-up
### Hardware
ESP32 board ("WeMos" D1 R32 in our case) with MicroPython.  
[Hardware layout](http://hobbycomponents.com/images/forum/wemos/Wemos_D1_HCWEMO0001_Diagram.png)  
[Pinout](https://cdn.instructables.com/FFU/YFXC/JIAJNA26/FFUYFXCJIAJNA26.LARGE.jpg)
#### Firmware
[MicroPython firmware download page](https://micropython.org/download#esp32)  
For purposes of our workshop, please download following: 
 - Download link 
    - Based on: [esp32-ppp-fix.bin](https://micropython.org/resources/firmware/esp32-ppp-fix.bin) (most recent today - 2019-05-23)
    - Embedded with uasyncio and aswitch libraries
    - With script to connect network and sync RTC via NTP on boot

### Software
#### Drivers
Windows: If the drivers for CH430 are not installed automatically, thay can be obtained [here ](https://wiki.wemos.cc/_media/ch341ser_win_3.4.zip)  
linux / MAC: ¯\\_(ツ)_/¯
#### IDE
[Thonny IDE](https://thonny.org/) was picked for this workshop. Reasons? Can be installed via pip, automatically detects and handles COM communication and allows us to flash firmware, so we don't have to utilize any other application.  
Getting the IDE: 
 - [Thonny IDE Download Page](https://github.com/thonny/thonny/releases)  
 or
 - `pip3 install thonny` and `python3 -m thonny`

Setting it up for ESP32:
 - install thonny-esp plug-in
    - Tools > Manage Plug-Ins > `thonny-esp`> install
    - restart Thonny IDE 
 - Tools > Options > Interpreter > MicroPython on ESP32

**More resources:**  
on IDE: [Thonny: The Beginner-Friendly Python Editor](https://realpython.com/python-thonny/)  
on using IDE with ESP: [Getting Started with Thonny MicroPython (Python) IDE for ESP32 and ESP8266](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/)



There are other IDEs, like [uPyCraft](http://docs.dfrobot.com/upycraft/) or you can utilize low-level approach via [ampy](https://github.com/pycampers/ampy) & [esptool](https://github.com/espressif/esptool/blob/master/README.md).  
[NodeMCU IDE comparison](https://frightanic.com/iot/tools-ides-nodemcu/)


## Input/Output
[io.py](io.py) - code related to following I/O operations
### Output
Built-in onboard LED is connected to Pin2. Let's try to turn it on and off.  
`>>> io.blink()`
### Input
#### Blocking
We're periodically checking for state change of the pin in a loop. Also the application won't respond to the user while it's running the loop. Although the functions sets both buttons, the program stucks on the checking loop for the first.  
`>>> io.test_blocking_input()`
#### Non-blocking, IRQ
Utilizes hardware interrupts. When state change on the pin is detected, interrupt is raised and calls the function binded to it.  
`>>> io.test_non_blocking_irq()`
#### Non-blocking, uasyncio
libraries needed: [uasyncio](https://github.com/peterhinch/micropython-async) and [aswitch](https://github.com/peterhinch/micropython-async/blob/master/aswitch.py). See [Sidenotes > Libraries installation](#libraries-installation)  
Takes advantage of asynchronous programming, which allows to run multiple tasks in parallel.  
aswitch library has built-in class for pushbutton, which correctly handles click, double-click, long press and filters out the button bounces.  
`asyncio.await()` in the `async_tick_tock()` pauses the cycle execution, so asyncio can run other tasks queued in the asyncio event loop.  
`>>> io.test_non_blocking_asyncio()`
## Connectivity
### Automatic WiFi connection and RTC clock sync
1. upload provided `wifi_and_ntp.py` into root directory on the ESP
1. make sure `config.py` contains correct `wifi_ssid` and `wifi_passwd`
1. add following 2 lines into `boot.py`, to have it executed on every board reboot and deepsleep wake
   ```py
   import wifi_and_ntp
   wifi_and_ntp.startup()
   ```
1. reboot the board
1. If performed correctly, it should automatically connect to the WiFi network, print IP config and perform synchronizaton on ESP RTC clocks with NTP

More details available [here](https://techtutorialsx.com/2017/06/06/esp32-esp8266-micropython-automatic-connection-to-wifi/)
### API calls
APIs (Application Programming Interfaces) are used to communicate between devices (IoT, servers, clients, ...). If offered to work with REST or SOAP API, politely decline SOAP and preffer REST.  
[Detailed introduction to general concept of APIs available here.](https://www.programmableweb.com/api-university/what-are-apis-and-how-do-they-work)
#### M2X
[AT&T M2X](http://m2x.att.com/) platform was chosen for this workshop for it's simplicity. Similar platforms supporting IoT integration could be [ThingSpeak](https://thingspeak.com/), [IFTTT](https://thingspeak.com/) and many others...  
&nbsp;  
[M2X API overview](https://m2x.att.com/developer/documentation/v2/overview)  
[M2X API cheatsheet](https://m2x.att.com/developer/documentation/v2/cheatsheet)  

#### Pre-set AT&T M2X devices
Few devices were created on the M2X platform for purposes of this workshop, so we can interface our ESP boards with a cloud service. Each of these devices has 2 data streams. One accepts numeric values only (`id:numeric`), the other custom strings (`id:non-numeric`). To reach API of these devices, we need `device_id` (to know which device to reach) and `api_key` (to authorize us).  

Dashboard to monitor workshop devices: [M2X AT&T Brno IoT training dashboard](https://m2x.att.com/dashboards/shared/5b4c39b189bbbc2469ba907df99cd6e6)
#### Request headers
Each network request has variable fields like headers, cookies, ... We don't need any cookies for this workshop, but will need to headers to:
 - `X-M2X-KEY` - authorize to the API
 - `Content-Type` - identify what type of data are we sending
 - `connection` - to indicate the connection can be closed once completed
 ```py
 headers = {
"X-M2X-KEY" : m2x_api_key,
"Content-Type" : "application/json",
"connection" : "close"
}
```

#### GET request
HTTP GET request is utilized to acquire data from the API.
```py
import urequests
url = "https://..."
response = urequests.get(url)
print(str(response.status_code), response.reason)
print(response.text)
```
[detailed guide for GET requests](https://techtutorialsx.com/2017/06/11/esp32-esp8266-micropython-http-get-requests/)

#### POST/PUT request
HTTP POST/PUT requests are used to send data to the API and create/update entries on the endpoint.  
Difference between POST and PUT: [IETF specs](https://techtutorialsx.com/2017/06/18/esp32-esp8266-micropython-http-post-requests/), [StackOverflow](https://stackoverflow.com/questions/630453/put-vs-post-in-rest)  
Difference in case of M2X platform:
 - POST - used to create resources (creation of new devices)
 - PUT - used to update resources (modifying streams of the device, submitting new values)  
 
```py
headers = {"Content-Type" : "application/json"}
payload = {"value" : "10"}
url = "https://..."

resp = urequests.put(url, data=json.dumps(payload), headers=headers)
print("request status:", str(resp.status_code), str(resp.reason))
print("Response - raw data:", resp.text)
```
[detailed guide for POST requests](https://techtutorialsx.com/2017/06/18/esp32-esp8266-micropython-http-post-requests/)



## Troubleshooting
###
**Error Numbers** https://github.com/micropython/micropython-lib/blob/master/errno/errno.py
#### `IndexError: list index out of range`
Any operation requiring operational network connection (NTP, API requests, ...) can throw `IndexError: list index out of range`  
**Solution**: Make sure your network connection is working properly.

#### Issues with urequests.put()
```py
> urequsts.put("https://....")

mbedtls_ssl_handshake error: -4290
Traceback (most recent call last):
  File "C:\Users\Fred\ESP\api_put.py", line 29, in <module>
  File "urequests.py", line 114, in put
  File "urequests.py", line 96, in request
  File "urequests.py", line 60, in request
OSError: [Errno 5] EIO
```
Application successfully sent one PUT request, then died with following error. Seems to be caused by lack of RAM on the ESP per [Issue#209](https://github.com/micropython/micropython-esp32/issues/209).  
 ```py  
OSError: 23
ENFILE = 23 # File table overflow
```
Application sent succesfully 10 requests. Failed on 11th.  
**Solution:**
Both issues requires manually calling `.close()` on the urequests session object prior starting a new request.  
Having `'connection' : 'close'`in request headers is not sufficient!
For multiple parallel HTTPS connections look for ESP32 with SPI RAM.

#### Queue issues with uasyncio
```py
Traceback (most recent call last):
  File "C:\Users\Fred\ESP\io.py", line 142, in <module>
  File "C:\Users\Fred\ESP\io.py", line 137, in test_non_blocking_asyncio
  File "/lib/uasyncio/core.py", line 168, in run_forever
  File "/lib/uasyncio/core.py", line 59, in call_later_ms
  File "/lib/uasyncio/core.py", line 64, in call_at_
IndexError: queue overflow

  File "/Users/dwhall/.micropython/lib/ufarc/__init__.py", line 513, in run_forever
  File "/Users/dwhall/.micropython/lib/ufarc/__init__.py", line 532, in stop
  File "uasyncio/core.py", line 183, in stop
  File "uasyncio/core.py", line 48, in call_soon
IndexError: full
```
When there is too much async events, the asyncio queue (utimeq) fills up. First overflows ([snippet source](https://github.com/dwhall/ufarc/)), then just states it's full and refuses to start. Reboot the board.  
You have to adjust size of the queue when you're setting up the asyncio loop. [src](https://forum.micropython.org/viewtopic.php?t=5908)  
`loop = asyncio.get_event_loop(runq_len=40, waitq_len=40)`


## Sidenotes
[MicroPython API reference](https://docs.micropython.org/en/latest/esp32/quickref.html)

### Libraries installation
**Automatic**  
```py
import upip
upip.install('micropython-uasyncio')
```
**Manual download**  
`%upload <source> <target>` is a Thonny IDE built-in command to transfer file from local to ESP
```
https://raw.githubusercontent.com/peterhinch/micropython-async/master/aswitch.py
%upload aswitch.py aswitch.py
```

### Memory management
```py
import gc
print('Free RAM: %.2f kB' % (gc.mem_free()/1024))
gc.collect()
print('Free RAM: %.2f kB' % (gc.mem_free()/1024))
```
### MD5 keys for devices
```py
import hashlib
devs = ["device0"+str(i) for i in range(0,10)]
hashes = [hashlib.md5(d.encode("utf-8")).hexdigest() for d in devs]
db = dict([(devs[i],hashes[i]) for i in range(0, len(devs))])
for d, h in db.items():
    print(d,h)
```
### Various utilities
(kept as notes for us for future use)  
https://www.apirequest.io/ - to perform API calls  
https://apitester.com/ - API calls, building test case scenarios  
https://curlbuilder.com/ - to build cURL queries  
https://onlinecurl.com/ - online cURL  
  
http://my-json-server.typicode.com - to build API out of github repository file (`db.json`)  
https://romannurik.github.io/SlidesCodeHighlighter/ - Allows source code highlighting and RTF copy&paste to M$ Office  
  
**Using ESP with JuPyter notebooks**  
https://towardsdatascience.com/micropython-on-esp-using-jupyter-6f366ff5ed9  
https://github.com/goatchurchprime/jupyter_micropython_kernel/  

#### Files in this repo
 - config files:
    - [`db.json`](db.json) - used by typicode service to have API to test against
    - [`config.py`](config.py)
       - `pin_btn1`, `pin_btn2` - hardware pins on which we connected the buttons
       - `ssid` - to which wi-fi network shall we connect? used for automatic connection
       - `passwd` - wi-fi password  
       - `m2x_device_id` - M2X device we're updating
       - `m2x_api_key` - device access key for the M2X
 - functional files 
    - [`wifi_and_ntp.py`](wifi_and_ntp.py) - utility for automatic wifi and ntp connection
    - [`io.py`](io.py) - hardware input/output related code
    - [`api_test.py`](api_test.py) - to test GET/PUT API calls against AT&T M2X (similar to ThingSpeak) service
