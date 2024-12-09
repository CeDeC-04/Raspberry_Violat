from classe_WIFI_bidireccional_PiESP32_20241201_5 import *
import time

wifi = WIFI()

wifi.WIFI_reinicia()

envia = '{"Pols_Llum_Cuina" : False}'
#time = WIFI.moduls_carregats["time"]
n = True

try:
    while True:
        print(wifi.WIFI_comunicacio(envia))
        time.sleep(1)
        if n:
            envia = '{"Pols_Llum_Cuina" : True}'
            n = False
        else:
            envia = '{"Pols_Llum_Cuina" : False}'
            n = True
except KeyboardInterrupt:
    print(f"Interromput per l'usiari")