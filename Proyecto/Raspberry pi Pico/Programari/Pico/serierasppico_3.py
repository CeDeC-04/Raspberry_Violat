from machine import UART, Pin
import utime

# Configura UART al Pico
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

while True:
    if uart.any():  # Comprova si hi ha dades entrants
        try:
            data = uart.read()  # Llegeix dades com a bytes
            print(f"Bytes rebuts: {data}")  # Mostra els bytes rebuts
            # Filtra només els bytes ASCII vàlids (32 a 127)
            filtered_data = bytes([b for b in data if 32 <= b <= 127])
            print(f"Dades filtrades: {filtered_data.decode('utf-8', errors='ignore').strip()}")
        except Exception as e:
            print(f"Error en manejar les dades: {e}")
    else:
        print("Esperant dades...")
    utime.sleep(1)
