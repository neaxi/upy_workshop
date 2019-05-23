# MicroPython workshop on ESP32 
## Set-up
### Hardware
ESP32 board ("WeMos" D1 R32 in our case) with MicroPython.
[Hardware layout](http://hobbycomponents.com/images/forum/wemos/Wemos_D1_HCWEMO0001_Diagram.png) 
[Pinout](https://cdn.instructables.com/FFU/YFXC/JIAJNA26/FFUYFXCJIAJNA26.LARGE.jpg)
#### Firmware
[MicroPython firmware download page](https://micropython.org/download#esp32)
For purposes of our workshop, please download following: 
 - Download link 
  -- Based on: [esp32-ppp-fix.bin](https://micropython.org/resources/firmware/esp32-ppp-fix.bin) (most recent today - 2019-05-23)
  -- Embedded with uasyncio and aswitch libraries
  -- With script to connect network and sync RTC via NTP on boot

### Software
#### Drivers
Windows: If the drivers for CH430 are not installed automatically, thay can be obtained [here ](https://wiki.wemos.cc/_media/ch341ser_win_3.4.zip)
linux / MAC: ¯\\_(ツ)_/¯
#### IDE
[Thonny IDE](https://thonny.org/) was picked for this workshop. Reasons? Can be installed via pip, automatically detects and handles COM communication and allows us to flash firmware, so we don't have to utilize any other application.
Getting the IDE: 
 - [Thonny IDE Download Page](https://github.com/thonny/thonny/releases)
 - `pip3 install thonny` and `python3 -m thonny`

Setting it up for ESP32:
 - install thonny-esp plug-in
  -- Tools > Manage Plug-Ins > `thonny-esp`> install
  -- restart Thonny IDE 
 - Tools > Options > Interpreter > ESP32

**More resources:**
on IDE: [Thonny: The Beginner-Friendly Python Editor](https://realpython.com/python-thonny/)
on using IDE with ESP: [Getting Started with Thonny MicroPython (Python) IDE for ESP32 and ESP8266](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/)



There are other IDEs, like [uPyCraft](http://docs.dfrobot.com/upycraft/) or you can utilize low-level approach via [ampy](https://github.com/pycampers/ampy) & [esptool](https://github.com/espressif/esptool/blob/master/README.md).
[NodeMCU IDE comparison](https://frightanic.com/iot/tools-ides-nodemcu/)


## Input/Output
### Output
### Input
#### Blocking
#### Non-blocking, IRQ
#### Non-blocking, uasyncio

## Connectivity
### Automatic WiFi connection and RTC clock sync


More details available [here](https://techtutorialsx.com/2017/06/06/esp32-esp8266-micropython-automatic-connection-to-wifi/)


## Troubleshooting
###
**Error Numbers** https://github.com/micropython/micropython-lib/blob/master/errno/errno.py
#### Issues with network connections
Any operation, that requires operational network connection (NTP, API requests, ...) can throw `IndexError: list index out of range`

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
Application successfully sent one PUT request, then died with following error. Seems to be caused by lack of RAM on the ESP per https://github.com/micropython/micropython-esp32/issues/209.
**Solution:** `.close()` the connection manually prior starting another request.  (For multiple parallel HTTPS connections look for ESP32 with SPI RAM )
  &nbsp;
 ```py  
OSError: 23
ENFILE = 23 # File table overflow
Close the connection with .close() when you're done with it.
'connection' : 'close' in headers is not sufficient
```
Application sent succesfully 10 requests. Failed on 11th.
**Solution:** Same as previous. Close each connection manually with `.close()` prior starting a new one.

Both issues requires manually calling `.close()` on the urequests session object. Having `'connection' : 'close'`in request headers is not sufficient!


## Sidenotes
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
 -- [`db.json`](db.json) - used by typicode service to have API to test against
 -- [`creds_m2x.py`](creds_m2x.py) - contains `api_key` and `device_id` used for M2X connections
 -- [`creds_wifi.py`](creds_wifi.py) - contains `ssid` and `passwd` used by auto-connection script
 - functional files 
 -- [`wifi_and_ntp.py`](wifi_and_ntp.py) - utility for automatic wifi and ntp connection
 -- [`io.py`](io.py) - hardware input/output related code
 -- [`api_test.py`](api_test.py) - to test GET/PUT API calls against AT&T M2X (similar to ThingSpeak) service
