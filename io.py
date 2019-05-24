import machine
import time

from aswitch import Pushbutton
import uasyncio as asyncio

# emergency exception buffer is created to handle ISR errors
# see https://docs.micropython.org/en/latest/reference/isr_rules.html#the-emergency-exception-buffer
import micropython
micropython.alloc_emergency_exception_buf(100)


# load from config on which pins we have the buttons 
try:
    from config import pin_btn01, pin_btn02
except:
    raise Exception("Failed to load button pin assignments from config")




# ----------------------------------------
# dummy print functions to demonstrate progress of the program
# ----------------------------------------
def tt():
    ''' dummy function, prints tick on even seconds, tock otherwise '''
    print("Tick" if time.localtime()[5] % 2 == 0 else "Tock", time.localtime()[5])


def tick_tock():
    ''' infinite ticking loop '''
    while(True):
        tt()    
        time.sleep(0.5)


async def async_tick_tock():
    ''' async variant of tick_tock, notice `await` in the loop '''
    while(True):
        tt()
        await asyncio.sleep(1)
        time.sleep(0.5)


def button_operation(pin, operation=None):
    ''' called when the button press is detected
        if called via IRQ, takes only 1 argument = pin on which the interrupt occurred
        if called as a normal function takes a string
    '''
    if isinstance(pin, machine.Pin):
        print("Interrupt received on", pin)
    elif isinstance(pin, str):
        print("{} was {}".format(pin,operation))




# ----------------------------------------
# Pin Output
# ----------------------------------------

def blink(pin=2):
    ''' put the pin in the HIGH state, wait 2 sec, LOW again
        pin 2 is the onboard LED
    '''
    out = machine.Pin(pin, machine.Pin.OUT)
    out.on()
    time.sleep(2)
    out.off()




# ----------------------------------------
# Pin Input
# ----------------------------------------

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
    



def non_blocking_irq(pin):
    btn = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
    btn.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_operation)
    
    
def test_non_blocking_irq():
    ''' first we register the button with the irq 
        then we run a tick_tock loop
        when the button is pressed, it will be visible in the loop printout
    '''    
    non_blocking_irq(pin_btn01)
    non_blocking_irq(pin_btn02)
    tick_tock()




async def test_btn(pin, suppress=True, lf=True, df=True):
    ''' handler for aswitch.Pushbutton instances '''
    pb = Pushbutton(pin, suppress)
    print('{} set up'.format(pin))
    pb.press_func(button_operation, (str(pin), "pushed",))
    pb.release_func(button_operation, (str(pin), "released",))    
    pb.double_func(button_operation, (str(pin), "double-clicked",))
    pb.long_func(button_operation, (str(pin), "long pressed",))


def test_non_blocking_asyncio():
    ''' creates two buttons (pin 18 and 19)
        then it starts the async loop
        adds handler for both buttons in the loop
        adds tick_tock to the loop to show its running
    '''
    pin18 = machine.Pin(pin_btn01, machine.Pin.IN, machine.Pin.PULL_UP)
    pin19 = machine.Pin(pin_btn02, machine.Pin.IN, machine.Pin.PULL_UP)

    loop = asyncio.get_event_loop(runq_len=40, waitq_len=40)
    asyncio.ensure_future(test_btn(pin18))
    asyncio.ensure_future(test_btn(pin19))
    asyncio.ensure_future(async_tick_tock())
    loop.run_forever()
