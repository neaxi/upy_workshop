import machine
import time

try:
    from config import pin_btn01, pin_btn02
except:
    raise Exception("Failed to load button pin assignments from config")
    


def blink(pin=2):
    ''' put the pin in the HIGH state, wait 2 sec, LOW again
        pin 2 is the onboard LED
    '''
    out = machine.Pin(pin, machine.Pin.OUT)
    out.on()
    time.sleep(2)
    out.off()
    
    
blink()