import serial
import time

# Configura el port UART
ser = serial.Serial('/dev/serial0', baudrate=4800, timeout=1)  # Redueix el baudrate a 4800

# Dona temps al Pico per estar llest
time.sleep(2)

try:
    while True:
        # Esborra els buffers abans d'enviar
        '''   ser.reset_input_buffer()
        ser.reset_output_buffer()

        # Envia un missatge al Pico
        message = "['hola' : 123]\n"  # Afegim un salt de línia per marcar el final del missatge
        try:
            ser.write(message.encode('utf-8'))
            print(f"Enviat: {message.strip()}")
        except serial.SerialException as e:
            print(f"Error d'escriptura: {e}")
            ser.close()
            time.sleep(1)
            ser.open()

        # Dorm una mica per evitar saturació al buffer del Pico
        time.sleep(2)

        while True:
            if ser.in_waiting > 0:
                llegit = ser.readline()
                try:
                    print("Dades rebudes:", llegit.decode().strip())
                except UnicodeDecodeError as e:
                    print(f"Error en desxifrar les dades: {e}")
                    print("Dades brutals (sense desxifrar):", llegit)
                
            else:
                break
        '''

        if ser.in_waiting > 0:
            #llegit = ser.readline()
            llegit = ser.read_all()
            print(llegit)
            try:
                print("Dades rebudes:A", llegit.decode().strip())
                print("Dades rebudes:B", llegit.decode())
            except UnicodeDecodeError as e:
                print(f"Error en desxifrar les dades: {e}")
                print("Dades brutals (sense desxifrar):", llegit)
        else:
            pass
            #print("Esperant dades...")
       # time.sleep(0.5)
except KeyboardInterrupt:
    print("Interromput per l'usuari.")
    ser.close()
