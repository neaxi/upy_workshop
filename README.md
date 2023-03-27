# MicroPython workshop on ESP32 
These information are not intended as a stand alone study material but rather as an aid and possible future reference for students which attended the AT&T Brno IoT workshop in person.
## Set-up
### Hardware
**"WeMos" D1 R32**  
 - [Datasheet](https://github.com/SmartArduino/ESPboard/blob/master/ESPduino-32s.pdf)  
 - [Hardware layout](http://hobbycomponents.com/images/forum/wemos/Wemos_D1_HCWEMO0001_Diagram.png)  
 - [Pinout](https://cpb-ap-se2.wpmucdn.com/blogs.auckland.ac.nz/dist/9/698/files/2021/08/2_Pinout_D1_R32.png)

**DevKitC**
 - [Homepage](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/hw-reference/esp32/get-started-devkitc.html)
 - [Schema](https://dl.espressif.com/dl/schematics/esp32_devkitc_v4-sch.pdf)
 - [Pinout](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/_images/esp32-devkitC-v4-pinout.png)

#### Firmware
[MicroPython firmware download page](https://micropython.org/download/esp32/)  
For purposes of our workshop, please download following: 
 - [Download our custom firmware](https://github.com/neaxi/upy_workshop/releases/download/untagged-e99e035402f888513f32/ESP32_ATTBrno_workshop_2022-11-09.zip)
    - Based on: [v1.19.1 (2022-06-18)](https://micropython.org/resources/firmware/esp32-20220618-v1.19.1.bin)
    - Embedded with uasyncio and aswitch libraries
    - With script to connect network and sync RTC via NTP on boot
#### Flashing firmware
Always erase the flash first, then install the new firmware.  
 a) From CLI via [esptool](https://github.com/espressif/esptool)
```
pip3 install esptool
python -m esptool --port COMx read_flash 0x00000 0x400000 firmware_image.bin
python -m esptool --port COMx --chip esp32 erase_flash
python -m esptool --port COMx --baud 921600 write_flash -z 0x1000 firmware_image_backup.bin
```

 b) Through Thonny IDE GUI
   Tools > Options > Interpreter > Install or update MicroPython

### Software
#### Drivers
Windows: if not installed automatically:
 - [CH340/341](https://github.com/HobbyComponents/CH340-Drivers/)  
 - [CP210x](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads)  

linux / MAC: ¯\\_(ツ)_/¯
#### IDE Setup
[Thonny IDE](https://thonny.org/) was picked for this workshop. Reasons? Can be installed via pip, automatically detects and handles serial port communication and allows us to flash firmware and upload files to the board, so we don't have to utilize any other application.  
Getting the IDE: 
 - [Thonny IDE Download Page](https://github.com/thonny/thonny/releases)  
 or
 - `pip3 install thonny` and `python3 -m thonny`

Change Thonny IDE to use MicroPython
 - Tools > Options > Interpreter > MicroPython (ESP32)
 - Tools > Options > Interpreter > Port or WebREPL > Select `COM` port of your device

In case we would want to download modules/libraries from PyPi:
 - Tools > Manage packages


**More resources:**  
on IDE: [Thonny: The Beginner-Friendly Python Editor](https://realpython.com/python-thonny/)  
on using IDE with ESP: [Getting Started with Thonny MicroPython (Python) IDE for ESP32 and ESP8266](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/)  
(please keep in mind older screenshot might not accurately represent current application)



There are other IDEs, like [uPyCraft](https://dfrobot.gitbooks.io/upycraft/content/) or you can utilize low-level approach via [ampy](https://github.com/pycampers/ampy) & [esptool](https://github.com/espressif/esptool/blob/master/README.md).  
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

#### ADC
Lets test analog input with a photoresistor.  
`ADC.read()` range: 12 bit ADC => 2<sup>12</sup> => 0-4095 values
```py
adc = ADC(Pin(34)) 
adc.atten(ADC.ATTN_11DB) # 3.3V range
print(adc.read()) # raw value 
print(adc.read()/4096 * 3.3) # coverted to voltage
```

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





#### Request headers
Each network request has variable fields like headers, cookies, ... Each API is different an you have to look into documentation on how to use it correctly.  
One of the most common headers is `Content-Type` which identifies what type of data are we sending, like `"application/json"`


#### GET request
HTTP GET request is utilized to acquire data from the API.  
Sample URL: http://my-json-server.typicode.com/neaxi/upy_workshop/
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
 
```py
headers = {"Content-Type" : "application/json"}
payload = {"value" : "10"}
url = "https://..."

resp = urequests.put(url, data=json.dumps(payload), headers=headers)
print("status:", str(resp.status_code), resp.reason)
print("Response - raw:", resp.text)
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
### MD5 keys for device names
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
 - functional files 
    - [`wifi_and_ntp.py`](wifi_and_ntp.py) - utility for automatic wifi and ntp connection
    - [`io.py`](io.py) - hardware input/output related code
    - [`api_test.py`](api_test.py) - to test GET/PUT API calls against API of IoT service
