from machine import Pin, SPI

# Configuració SPI
spi = SPI(0, baudrate=10000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)

# Buffer per rebre dades
buffer = bytearray(5)

while True:
    cs.off()  # Activa el Slave
    spi.readinto(buffer)  # Llegeix dades
    cs.on()  # Desactiva el Slave
    print(f"Dades rebudes: {list(buffer)}")
