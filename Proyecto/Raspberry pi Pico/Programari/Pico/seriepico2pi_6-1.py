from machine import UART, Pin
import utime

# Configura UART al Pico
uart = UART(0, baudrate=4800, tx=Pin(0), rx=Pin(1))  # Configura Tx i Rx amb baudrate de 4800

# Dona temps a la Raspberry Pi per estar llesta
utime.sleep(2)

try:
    while True:
        # Esborra el buffer d'escriptura abans d'enviar (si hi ha dades acumulades)
        while uart.any():
            uart.read()  # Buida el buffer d'entrada

        # Envia un missatge a la Raspberry Pi
        message = "123\n"  # Afegim un salt de línia per marcar el final del missatge
        try:
            uart.write(message)  # Envia el missatge
            print(f"Enviat: {message.strip()}")
        except Exception as e:
            print(f"Error d'escriptura: {e}")

        # Dorm una mica per evitar saturació al buffer de la Raspberry Pi
        utime.sleep(2)
except KeyboardInterrupt:
    print("Interromput per l'usuari.")
