'''import spidev
import time

# Configurar SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus SPI 0, dispositiu 0
spi.max_speed_hz = 50000
spi.mode = 0

# Enviar i rebre dades
while True:
    message_to_send = "Hola Pico!"  # Missatge simple
    data_to_send = list(message_to_send.encode('utf-8'))[:64]  # Convertir a bytes, max 64 bytes
    while len(data_to_send) < 64:  # Omplir amb zeros fins a 64 bytes
        data_to_send.append(0)
    
    print(f"Enviant: {message_to_send}")
    response = spi.xfer(data_to_send)  # Enviar dades i rebre resposta
    response_str = ''.join([chr(b) for b in response if b != 0])  # Convertir bytes a text

    print(f"Resposta de la Pico: {response_str}")
    time.sleep(1)
'''

import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, CE0
spi.max_speed_hz = 50000

print("Enviant dades a la Pico...")

while True:
    try:
        response = spi.xfer([0x01, 1x02, 0x03])  # Envia 3 bytes simples
        print(f"Dades rebudes de la Pico: {response}")
        time.sleep(1)
    except KeyboardInterrupt:
        print("Finalitzant...")
        spi.close()
        break
