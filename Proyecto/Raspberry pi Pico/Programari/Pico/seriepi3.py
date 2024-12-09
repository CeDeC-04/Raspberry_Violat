import serial
import time

# Configura el port UART
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

try:
    while True:
        # Envia un missatge al Pico
        message = "123"
        ser.write(message.encode('utf-8'))
        print(f"Enviat: {message.strip()}")
        
        # Llegeix la resposta
        # response = ser.readline().decode('utf-8', errors= 'ignore').strip()
        #if response:
        #    print(f"Resposta rebuda: {response}")
        
        time.sleep(1)
except KeyboardInterrupt:
    print("Interromput per l'usuari.")
    ser.close()
