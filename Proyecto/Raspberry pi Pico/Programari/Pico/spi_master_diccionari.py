import spidev
import time
import json

# Configurar SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus SPI 0, dispositiu 0
spi.max_speed_hz = 50000
spi.mode = 0

# Crear un diccionari
data = {"temperatura": 25, "humitat": 60, "estat": "OK"}

# Convertir el diccionari a una cadena JSON i després a bytes
data_bytes = json.dumps(data).encode('utf-8')

# Enviar el diccionari com a bytes
while True:

    print("Dades a enviar:", data_bytes)

    response = spi.xfer(list(data_bytes))  # Enviar i rebre dades
    print("Resposta de la Pico:", response)
    time.sleep(1)  # Esperar 1 segon
