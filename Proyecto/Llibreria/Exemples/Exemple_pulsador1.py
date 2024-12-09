from classe_LED import *
from classe_pulsador import *

led = LED(17, 5, "pi_3")
led2 = LED(27, 0, "pi_3")
pulsador = Pulsador(4, False, "pi_3")

try:
    while True:
        if pulsador.temps_pulsat(2):
            led.treu_intensitat()
            led2.aumenta_intensitat()
            time.sleep(0.1)
        
except KeyboardInterrupt:
    led.cleanup()
    led2.cleanup()
    pulsador.cleanup()