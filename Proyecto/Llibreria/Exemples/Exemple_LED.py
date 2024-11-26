from classe_LED import *
from classe_pulsador import *

led = LED(17, 3)
led2 = LED(27, 1)

try:
    while True:
        led.alterna()
        time.sleep(2)
        led2.alterna()
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()