#Codi de prova communicació
import spidev
import time

# Configurar SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus SPI 0, dispositiu 0 (el primer dispositiu SPI)
spi.max_speed_hz = 50000  # Velocitat de comunicació
spi.mode = 0  # Mode SPI (polarity=0, phase=0)

# Enviar dades
while True:
    message = [0x01, 0x02, 0x03]  # Missatge a enviar
    response = spi.xfer(message)  # Enviar i rebre dades
    print("Resposta de la Pico:", response)
    time.sleep(1)  # Esperar 1 segon
