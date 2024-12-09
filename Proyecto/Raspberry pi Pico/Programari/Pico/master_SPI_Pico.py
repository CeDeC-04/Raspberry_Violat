from machine import Pin, SPI
import utime

# Configura el bus SPI0
spi = SPI(0, baudrate=50000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)  # Chip Select

# Funció per enviar i rebre dades
def send_and_receive(data):
    cs.off()  # Activa el Slave
    response = bytearray(len(data))
    spi.write_readinto(bytearray(data), response)  # Envia i rep dades
    cs.on()  # Desactiva el Slave
    return list(response)

try:
    while True:
        # Dades a enviar
        to_send = [1, 2, 3, 4, 5]
        print(f"Enviant dades: {to_send}")
        
        # Envia les dades i rep resposta
        response = send_and_receive(to_send)
        print(f"Resposta del Slave: {response}")
        
        utime.sleep(1)
except KeyboardInterrupt:
    print("Interromput per l'usuari")
