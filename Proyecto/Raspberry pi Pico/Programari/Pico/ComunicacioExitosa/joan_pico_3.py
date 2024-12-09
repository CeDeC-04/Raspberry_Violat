from machine import UART, Pin
import utime

# Configura UART al Pico
uart = UART(0, baudrate=4800, tx=Pin(0), rx=Pin(1))

# Dona temps a la Raspberry per estar llesta
utime.sleep(2)

try:
    while True:
        # PART 1: Rebre un missatge de la Raspberry
        if uart.any():  # Comprova si hi ha dades entrants
            try:
                data = uart.read()  # Llegeix les dades entrants
                print(f"Bytes rebuts: {data}")
                # Filtra només els bytes ASCII vàlids (32 a 127)
                filtered_data = bytes([b for b in data if 32 <= b <= 127])
                if filtered_data:
                    decoded_data = filtered_data.decode('utf-8').strip()
                    print(f"Dades rebudes: {decoded_data}")
            except Exception as e:
                print(f"Error en manejar les dades: {e}")

        # PART 2: Enviar un missatge a la Raspberry
        message = "Hola Raspberry!\n"
        try:
            uart.write(message)
            print(f"Enviat: {message.strip()}")
        except Exception as e:
            print(f"Error d'escriptura: {e}")

        # Dorm una mica abans del següent cicle
        utime.sleep(2)
except KeyboardInterrupt:
    print("Interromput per l'usuari.")




