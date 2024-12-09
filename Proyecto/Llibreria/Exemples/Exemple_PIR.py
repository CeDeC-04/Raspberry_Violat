from classe_PIR import *
import time

P = SensorPIR(4)

print(P)

try:
    while True:
        if P.detecta_moviment():
            print("ATENCIÓ ALARMA!!!!!!")
        time.sleep(0.25)
            
except KeyboardInterrupt:
    pass
