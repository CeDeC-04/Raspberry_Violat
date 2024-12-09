from classe_MQ2 import *

sensor = MQ2(18, "pi_3")
try:
    while True:
        if sensor.detecta_particules():
            print("Gas detectado!")
        else:
            print("No se detecta gas.")
        time.sleep(1)
except KeyboardInterrupt:
    sensor.cleanup()