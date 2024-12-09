from machine import Pin, SPI
import utime

# Configura el bus SPI0
spi = SPI(0, baudrate=50000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.IN, Pin.PULL_UP)  # Chip Select

buffer = bytearray(5)  # Buffer per rebre dades

try:
    while True:
        if not cs.value():  # Activa quan CS està baix
            spi.readinto(buffer)  # Llegeix dades enviades pel Master
            print(f"Dades rebudes del Master: {list(buffer)}")
            
            # Processa les dades i prepara una resposta
            response = [x + 1 for x in buffer]  # Incrementa cada valor
            print(f"Enviant resposta al Master: {response}")
            
            cs.off()  # Simula el control del Slave
            spi.write(bytearray(response))  # Envia la resposta al Master
            cs.on()
            
            utime.sleep(0.1)
except KeyboardInterrupt:
    print("Interromput per l'usuari")
