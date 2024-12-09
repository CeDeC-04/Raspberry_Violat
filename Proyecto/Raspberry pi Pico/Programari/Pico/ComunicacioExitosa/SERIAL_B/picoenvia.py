from machine import UART, Pin
import utime

# Configura UART al Pico
uart = UART(0, baudrate=4800, tx=Pin(0), rx=Pin(1))

# Funció per netejar el buffer UART
def clear_uart_buffer():
    while uart.any():
        uart.read()  # Llegeix i descarta qualsevol dada pendent

# Dona temps al receptor per estar llest
utime.sleep(2)

# Neteja el buffer UART abans de començar
clear_uart_buffer()

while True:
    try:
        # Missatge a enviar
        message = "['Hola Mamona' : 52]\n"
        clear_uart_buffer()  # Assegura't que el buffer està buit abans d'enviar
        uart.write(message)  # Envia el missatge
        print(f"Enviat: {message.strip()}")
    except Exception as e:
        print(f"Error en enviar dades: {e}")
    utime.sleep(1)  # Espera entre enviaments
