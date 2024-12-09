from machine import Pin
import time

# Configura el LED al pin GPIO2
led = Pin(2, Pin.OUT)

while True:
    led.value(1)  # Encén el LED
    time.sleep(1) # Espera 1 segon
    led.value(0)  # Apaga el LED
    time.sleep(1) # Espera 1 segon