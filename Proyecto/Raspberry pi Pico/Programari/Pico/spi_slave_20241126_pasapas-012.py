from machine import Pin, SPI
import time

spi = SPI(0, baudrate=50000, polarity=0, phase=0, bits=8)
cs = Pin(17, Pin.IN, Pin.PULL_UP)
i = 0
while True:
    if not cs.value():  # CS actiu
        data = spi.read(1)  # Llegeix 1 byte
        print("Dades rebudes:", data, i)
        spi.write(b'\xAA')  # Envia un byte com a resposta
    i += 1
