import serial
import time

# Configura el port UART
ser = serial.Serial('/dev/serial0', baudrate=4800, timeout=1)

# Dona temps al Pico per estar llest
time.sleep(2)

try:
    while True:
        # PART 1: Enviar un missatge al Pico
        ser.reset_input_buffer()  # Neteja el buffer d'entrada
        ser.reset_output_buffer()  # Neteja el buffer de sortida
        message = "Hola Pico!\n"
        try:
            ser.write(message.encode('utf-8'))
            print(f"Enviat: {message.strip()}")
        except serial.SerialException as e:
            print(f"Error d'escriptura: {e}")
            ser.close()
            time.sleep(1)
            ser.open()

        # PART 2: Rebre un missatge del Pico
        try:
            if ser.in_waiting:  # Comprova si hi ha dades entrants
                data = ser.read(ser.in_waiting)
                print(f"Bytes rebuts: {data}")
                filtered_data = bytes([b for b in data if 32 <= b <= 127])
                if filtered_data:
                    decoded_data = filtered_data.decode('utf-8').strip()
                    print(f"Dades rebudes: {decoded_data}")
        except Exception as e:
            print(f"Error en manejar les dades: {e}")

        # Dorm una mica abans del següent cicle
        time.sleep(2)
except KeyboardInterrupt:
    print("Interromput per l'usuari.")
    ser.close()
