import serial
import time

# Configura el port UART
ser = serial.Serial('/dev/serial0', baudrate=4800, timeout=1)

# Dona temps al Pico per estar llest
time.sleep(2)

try:
    while True:
        if ser.in_waiting > 0:  # Comprova si hi ha dades disponibles
            # Captura i mostra bytes rebuts
            data = ser.readline()
            print(f"Bytes bruts rebuts: {data}")

            try:
                # Decodifica i mostra el missatge
                decoded_data = data.decode('utf-8').strip()
                print(f"Rebut: {decoded_data}")
            except UnicodeDecodeError as e:
                print(f"Error de decodificació: {e}")
except KeyboardInterrupt:
    print("Finalitzat per l'usuari.")
    ser.close()
