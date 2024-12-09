'''from machine import Pin, SPI
import time

# Configurar SPI com a esclau
spi = SPI(0, baudrate=50000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
cs = Pin(17, Pin.IN, Pin.PULL_UP)  # Pin de selecció de dispositiu (CS)

while True:
    if not cs.value():  # Si CS està actiu
        # Llegir dades del Master
        received_message = spi.read(64)  # Llegir fins a 64 bytes
        message_str = ''.join([chr(b) for b in received_message if b != 0])  # Convertir bytes a text
        print(f"Dades rebudes: {message_str}")

        # Enviar resposta al Master
        response_message = "Hola Pi!"  # Missatge de resposta
        response_bytes = list(response_message.encode('utf-8'))[:64]  # Convertir a bytes
        while len(response_bytes) < 64:  # Omplir amb zeros
            response_bytes.append(0)

        spi.write(bytearray(response_bytes))  # Enviar resposta
        print(f"Resposta enviada: {response_message}")
'''


from machine import Pin, SPI

spi = SPI(0, baudrate=50000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
cs = Pin(17, Pin.IN, Pin.PULL_UP)  # CS a GPIO 17

print("Esperant dades des del Master...")

while True:
    if not cs.value():
        message = spi.read(3)  # Llegeix 3 bytes
        print(f"Dades rebudes del Master: {message}")
        spi.write(bytearray([0xAA, 0xAA, 0xCC]))  # Respon
