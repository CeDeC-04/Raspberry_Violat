from machine import UART, Pin
import utime

# Configura UART al Pico
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Funció per netejar el buffer inicial
def clear_uart_buffer():
    while uart.any():
        uart.read()  # Esborra qualsevol dada restant

# Esborrem el buffer inicial abans de començar
clear_uart_buffer()

while True:
    if uart.any():  # Comprova si hi ha dades entrants
        try:
            data = uart.read()  # Llegeix les dades com a bytes
            print(f"Bytes rebuts: {data}")  # Mostra els bytes crus per depurar

            # Intentem decodificar les dades manualment
            try:
                decoded_data = data.decode('utf-8').strip()  # Decodifica sense paràmetres extra
                print(f"Dades decodificades: {decoded_data}")
            except Exception as e:
                print(f"Error de decodificació: {e}")
                
        except Exception as e:
            print(f"Error en manejar les dades: {e}")
    else:
        print("Esperant dades...")  # Missatge per indicar que no arriben dades
    utime.sleep(0.2)  # Redueix el temps d'espera per llegir més sovint

