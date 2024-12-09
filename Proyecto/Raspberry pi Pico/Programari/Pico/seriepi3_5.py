import serial
import time

# Configura el port UART
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

# Dona temps al Pico per estar llest
time.sleep(2)

try:
    while True:
        # Esborra el buffer d'entrada i sortida abans d'enviar
        ser.reset_input_buffer()  # Neteja qualsevol dada antiga
        ser.reset_output_buffer()  # Neteja dades residuals d'escriptura

        # Envia un missatge al Pico
        message = "123\n"  # Afegim un salt de línia per marcar final del missatge
        try:
            ser.write(message.encode('utf-8'))
            print(f"Enviat: {message.strip()}")
        except serial.SerialException as e:
            print(f"Error d'escriptura: {e}")
            ser.close()
            time.sleep(1)
            ser.open()

        # Dorm una mica per evitar saturació del buffer
        time.sleep(2)
except KeyboardInterrupt:
    print("Interromput per l'usuari.")
    ser.close()
