from machine import Pin, SPI
import utime

# Configuració del bus SPI
spi = SPI(0, baudrate=50000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)

# Buffer per rebre dades
buffer = bytearray(5)

while True:
    cs.off()  # Selecciona el dispositiu
    spi.readinto(buffer)  # Llegeix les dades enviades
    cs.on()  # Desselecciona el dispositiu
    
    # Mostra les dades rebudes
    print(f"Dades rebudes: {list(buffer)}")
    
    # Processa les dades i crea una resposta (aquí només les retorna incrementades)
    response = [x + 1 for x in buffer]
    print(f"Enviant resposta: {response}")
    
    # Envia la resposta
    cs.off()
    spi.write(bytearray(response))
    cs.on()
    
    utime.sleep(1)
