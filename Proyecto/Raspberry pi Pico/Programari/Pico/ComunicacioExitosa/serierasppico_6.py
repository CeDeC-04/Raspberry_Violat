from machine import UART, Pin
import utime

# Configura UART al Pico
uart = UART(0, baudrate=4800, tx=Pin(0), rx=Pin(1))  # Baudrate ajustat a 4800

# Dona temps a l'altre dispositiu per estar llest
utime.sleep(2)

while True:
    try:
        # Missatge a enviar
        message = "123\n"
        uart.write(message)  # Envia el missatge
        print(f"Enviat: {message.strip()}")
    except Exception as e:
        print(f"Error en enviar dades: {e}")
    utime.sleep(2)  # Espera entre enviaments per evitar saturació
