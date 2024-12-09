import spidev
import time

# Configura SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, dispositiu 0 (pins SPI predeterminats)
spi.max_speed_hz = 10000  # Velocitat del bus SPI

def send_and_receive(data):
    # Envia dades i rep la resposta
    response = spi.xfer2(data)
    return response

try:
    while True:
        # Dades per enviar (byte array)
        to_send = [1, 2, 3, 4, 5]
        print(f"Enviant dades: {to_send}")
        
        # Envia dades i espera resposta
        response = send_and_receive(to_send)
        print(f"Resposta rebuda: {response}")
        
        time.sleep(1)
except KeyboardInterrupt:
    print("Interromput per l'usuari")
finally:
    spi.close()
