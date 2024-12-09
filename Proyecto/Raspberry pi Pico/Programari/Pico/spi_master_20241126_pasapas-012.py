import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # Bus SPI 0, Device 0
spi.max_speed_hz = 50000
i=0
while True:
    resp = spi.xfer([0x42])  # Envia un byte, espera resposta
    print("Resposta:", resp, i)
    time.sleep(1)
    i += 1
