import serial
import time

# Configura el port UART
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

try:
    while True:
        #message = "Hola des de la Raspberry Pi!\n"  # Missatge simple
        #ser.write(message.encode('utf-8'))  # Envia el missatge codificat com UTF-8
        #print(f"Enviat: {message.strip()}")
        #ser.reset_input_buffer()
        #ser.reset_output_buffer()
        ser.write(b"Test\n")  # Envia un missatge senzill com a bytes crus
        time.sleep(1)
except KeyboardInterrupt:
    print("Interromput per l'usuari.")
    ser.close()
