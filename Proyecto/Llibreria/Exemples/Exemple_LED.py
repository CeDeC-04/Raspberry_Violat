from classe_LED import *

led = LED(17, 3, "pi_3")
led2 = LED(27, 1, "pi_3")

try:
    while True:
        led.alterna()
        print(led.intensitat)
        time.sleep(2)
        led2.alterna()
        print(led2.intensitat)
        time.sleep(2)
except KeyboardInterrupt:
    led.cleanup()
    led2.cleanup()