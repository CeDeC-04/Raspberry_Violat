from classe_DHT11 import *

S = DHT11(14)

print(S)
try:
    while True:
        print('sensor', S.llegeix_sensor())
        time.sleep(1)
        print('humitat', S.llegeix_humitat())
        time.sleep(1)
        print('temperatura', S.llegeix_temperatura())
        time.sleep(1)
except KeyboardInterrupt:
    pass
