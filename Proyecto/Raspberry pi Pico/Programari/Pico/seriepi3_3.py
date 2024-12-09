import serial
import time

# Configura el port UART
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

try:
    while True:
        # Esborra el buffer abans d'enviar
        ser.reset_output_buffer()

        # Envia un missatge al Pico
        message = "123"
        try:
            ser.write(message.encode('utf-8'))
            print(f"Enviat: {message.strip()}")
        except serial.SerialException as e:
            print(f"Error d'escriptura: {e}")
            ser.close()
            time.sleep(1)
            ser.open()

        # Dorm una mica més per evitar saturació
        time.sleep(2)
except KeyboardInterrupt:
    print("Interromput per l'usuari.")
    ser.close()
