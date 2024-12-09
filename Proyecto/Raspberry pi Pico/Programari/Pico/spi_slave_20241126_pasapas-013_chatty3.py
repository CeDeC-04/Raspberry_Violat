from machine import Pin, SPI

spi = SPI(0, baudrate=50000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(17, Pin.OUT)

while True:
    cs.off()
    spi.write(bytearray([9, 9, 9, 9, 9]))  # Envia resposta fixa
    cs.on()
