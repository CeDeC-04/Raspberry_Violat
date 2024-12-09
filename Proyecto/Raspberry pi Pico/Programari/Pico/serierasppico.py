from machine import UART, Pin
import utime

# Configura UART al Pico
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

while True:
    # Esborra el buffer si hi ha dades pendents
    #while uart.any():
    #    uart.read()  # Esborra les dades pendents

    # Comprova si hi ha dades noves entrants
    if uart.any():
        data = uart.read()  # Llegeix les dades rebudes
        print(data)
        #print(f"Dades rebudes: {data.decode('utf-8', errors='ignore').strip()}")
        
        # Respon al Master
        #response = "Resposta del Pico!\n"
        #uart.write(response)
        #print(f"Resposta enviada: {response.strip()}")
    utime.sleep(1)
