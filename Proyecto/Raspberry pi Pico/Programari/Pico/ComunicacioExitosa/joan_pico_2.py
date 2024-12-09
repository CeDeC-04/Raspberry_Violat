from machine import UART, Pin
import utime

# Configura UART al Pico
uart = UART(0, baudrate=4800, tx=Pin(0), rx=Pin(1))

def clear_uart_buffer():
    """
    Neteja completament el buffer del UART abans d'enviar.
    """
    while uart.any():  # Comprova si hi ha dades al buffer
        uart.read()  # Llegeix i descarta tot el contingut del buffer

# Dona temps inicial per assegurar la configuració
utime.sleep(2)

try:
    while True:
        # Neteja el buffer abans d'enviar
        clear_uart_buffer()

        # Envia un missatge
        message = "Hola Raspberry!\n"  # Missatge delimitat amb \n
        try:
            uart.write(message.encode('utf-8'))  # Assegurem la codificació UTF-8
            print(f"Enviat: {message.strip()}")
        except Exception as e:
            print(f"Error d'escriptura: {e}")

        # Dorm una mica abans del següent cicle
        utime.sleep(2)
except KeyboardInterrupt:
    print("Interromput per l'usuari.")



