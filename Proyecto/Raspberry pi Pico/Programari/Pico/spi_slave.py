from machine import Pin, SPI
import time

# Configurar SPI com a esclau
spi = SPI(0, baudrate=50000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
cs = Pin(17, Pin.IN, Pin.PULL_UP)  # Pin de selecció de dispositiu (CS)

# Funció per processar les dades que rebem
def procesar_dades():
    # Espera a que el master enviï dades
    if not cs.value():  # Comprova si el pin de selecció (CS) està actiu
        message = spi.read(3)  # Llegir 3 bytes des del master
        print("Missatge rebut:", message)
        spi.write(bytearray([0x10, 0x20, 0x30]))  # Resposta al master

while True:
    procesar_dades()  # Comprovem si hi ha missatges i els processem
    time.sleep(0.1)   # Espera per no sobrecarregar el processador
