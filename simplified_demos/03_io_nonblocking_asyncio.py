import machine
import time

from aswitch import Pushbutton
import uasyncio as asyncio

# load from config on which pins we have the buttons
try:
    from config import pin_btn01, pin_btn02
except:
    raise Exception("Failed to load button pin assignments from config")


def tick_tock():
    """dummy function, prints tick on even seconds, tock otherwise"""
    text = "Tock"
    if time.localtime()[5] % 2 == 0:
        text = "Tick"
    print(text)

async def ticking_loop():
    """async variant of tick_tock, notice `await` in the loop"""
    while True:
        tick_tock()
        await asyncio.sleep(1)
        


def button_operation(pin, operation=None):
    """called when the button press is detected"""
    print("{} was {}".format(pin, operation))
    
    
    

async def test_btn(pin, suppress=True, lf=True, df=True):
    """handler for aswitch.Pushbutton instances"""
    pb = Pushbutton(pin, suppress)
    print('{} set up'.format(pin))
    pb.press_func(button_operation, (str(pin), "pushed",))
    pb.release_func(button_operation, (str(pin), "released",))    
    pb.double_func(button_operation, (str(pin), "double-clicked",))
    pb.long_func(button_operation, (str(pin), "long pressed",))


def test_non_blocking_asyncio():
    """creates two buttons (pin 18 and 19)
    then it starts the async loop
    adds handler for both buttons in the loop
    adds tick_tock to the loop to show its running
    """
    pin1 = machine.Pin(pin_btn01, machine.Pin.IN, machine.Pin.PULL_UP)
    pin2 = machine.Pin(pin_btn02, machine.Pin.IN, machine.Pin.PULL_UP)
    
    loop = asyncio.get_event_loop(runq_len=40, waitq_len=40)
    asyncio.create_task(test_btn(pin1))
    asyncio.create_task(test_btn(pin2))
    asyncio.create_task(ticking_loop())
    loop.run_forever()


test_non_blocking_asyncio()
