import machine
import time

# load from config on which pins we have the buttons 
try:
    from config import pin_btn01, pin_btn02
except:
    raise Exception("Failed to load button pin assignments from config")
    
# emergency exception buffer is created to handle ISR errors
# see https://docs.micropython.org/en/latest/reference/isr_rules.html#the-emergency-exception-buffer
import micropython
micropython.alloc_emergency_exception_buf(100)



def tick_tock():
    """dummy function, prints tick on even seconds, tock otherwise"""
    text = "Tock"
    if time.localtime()[5] % 2 == 0:
        text = "Tick"
    print(text)

def ticking_loop():
    while True:
        tick_tock()
        time.sleep(1)



def button_operation(pin):
    """called when the button press is detected
    if called via IRQ, takes only 1 argument = pin on which the interrupt occurred
    """
    print("Interrupt received on", pin)


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
    ticking_loop()
    
test_non_blocking_irq()
