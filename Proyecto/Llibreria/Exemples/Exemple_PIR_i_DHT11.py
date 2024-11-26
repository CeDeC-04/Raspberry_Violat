from classe_DHT11 import *
from classe_PIR import *

S = DHT11(14)
P = SensorPIR(4)

print(S)
print(P)
try:
    while True:
        if P.detecta_moviment():
            print(f"A la sala hi ha una temperatura i humitat:\n"
                  f" {S.llegeix_sensor()[0]} ºC\n"
                  f" {S.llegeix_sensor()[1]} %H")
            '''print('sensor', S.llegeix_sensor())
            print('humitat', S.llegeix_humitat())
            print('temperatura', S.llegeix_temperatura())'''
            
except KeyboardInterrupt:
    pass
