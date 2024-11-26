from classe_LED import *
from classe_pulsador import *

pulsador = Pulsador(4, False)

try:
    while True:
        if pulsador.unica_pulsacio():
            print("Pulsacio detectada")
            time.sleep(0.3)
        
except KeyboardInterrupt:
    pulsador.cleanup()