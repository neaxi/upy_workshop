import machine
import time


# load from config on which pins we have the buttons 
try:
    from config import pin_btn01, pin_btn02
except:
    raise Exception("Failed to load button pin assignments from config")


def blocking_input(pin):
    ''' periodically reads state of the pin
        application does not respond, while .sleep() is running
    '''
    button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
    while(True):
        # When the button is pushed, it connects the pin with GND, pin.value() returns 0 (= logic LOW)
        # not(button.value()) causes LOW = True, HIGH = False
        button_state = "pushed" if not(button.value()) else "released"
        print("Button on pin {} is {}".format(pin, button_state))
        time.sleep(0.1)


def test_blocking_input():
    blocking_input(pin_btn01)
    blocking_input(pin_btn02)
    

test_blocking_input()