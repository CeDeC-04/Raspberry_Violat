from classe_FC51 import *

infrarrojo = SensorInfrarrojo(4)

try:
    while True:
        if infrarrojo.detecta_obstacle():
            print("Obstaculo detectado!!!")
        time.sleep(0.25)
            
except KeyboardInterrupt:
    infrarrojo.cleanup()