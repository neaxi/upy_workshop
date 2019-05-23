import machine
import time

from aswitch import Pushbutton
import uasyncio as asyncio


def tt():
    ''' dummy function, prints tick on even seconds, tock otherwise '''
    print("Tick" if time.localtime()[5] % 2 == 0 else "Tock", time.localtime()[5])

def tick_tock():
    while(True):
        tt()    
        time.sleep(0.5)

async def a_tick_tock():
    ''' async variant of tick_tock, notice `await` in the loop '''
    while(True):
        tt()
        await asyncio.sleep(1)
        time.sleep(0.5)

def blink(pin):
    ''' put the pin in the HIGH state, wait 2 sec, LOW again '''
    out = machine.Pin(pin, machine.Pin.OUT)
    out.on()
    time.sleep(2)
    out.off()


def blocking_input(pin):
    ''' periodically reads state of the pin
        application does not respond, while .sleep() is running
    '''
    button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
    while(True):
        print(button.value())
        time.sleep(0.1)


def button_operation(pin, operation=None):
    ''' called when the button press is detected '''
    print("{} was {}".format(pin,operation))


def non_blocking_irq(pin):
    ''' first we register the button with the irq 
        then we run a tick_tock loop
        when the button is pressed, it will be visible in the loop printout
    '''
    btn = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
    btn.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_operation)
    tick_tock()


async def test_btn(pin, suppress=True, lf=True, df=True):
    ''' handler for aswitch.Pushbutton instances '''
    pb = Pushbutton(pin, suppress)
    print('pin {} set up'.format(pin))
    pb.press_func(button_operation, (pin, "pushed",))
    pb.release_func(button_operation, (pin, "released",))    
    pb.double_func(button_operation, (pin, "double-clicked",))
    pb.long_func(button_operation, (pin, "long pressed",))


def non_blocking_asyncio():
    ''' creates two buttons (pin 18 and 19)
        then it starts the async loop
        adds handler for both buttons in the loop
        adds tick_tock to the loop to show its running
    '''
    pin18 = Pin(18, Pin.IN, Pin.PULL_UP)
    pin19 = Pin(19, Pin.IN, Pin.PULL_UP)

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(test_btn(pin18))
    asyncio.ensure_future(test_btn(pin19))
    asyncio.ensure_future(a_tick_tock())
    loop.run_forever()
