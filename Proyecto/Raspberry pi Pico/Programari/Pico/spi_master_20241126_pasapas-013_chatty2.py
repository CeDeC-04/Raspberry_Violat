import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Dispositiu 0
spi.max_speed_hz = 10000

def send_and_receive(data):
    print(f"Enviant: {data}")
    response = spi.xfer2(data)
    print(f"Rebuda: {response}")
    return response

try:
    while True:
        send_and_receive([1, 2, 3, 4, 5])
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
