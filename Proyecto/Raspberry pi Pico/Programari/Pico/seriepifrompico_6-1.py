import serial
import time

# Configura el port UART
ser = serial.Serial('/dev/serial0', baudrate=4800, timeout=1)  # Configura el baudrate a 4800

# Funció per netejar el buffer inicial
def clear_uart_buffer():
    while ser.in_waiting:
        ser.read(ser.in_waiting)  # Esborra qualsevol dada restant al buffer

# Esborrem el buffer inicial abans de començar
clear_uart_buffer()

try:
    while True:
        if ser.in_waiting:  # Comprova si hi ha dades entrants
            try:
                # Llegeix totes les dades disponibles
                data = ser.read(ser.in_waiting)
                print(f"Bytes rebuts: {data}")  # Mostra els bytes crus

                # Filtra bytes vàlids (ASCII entre 32 i 127)
                filtered_data = bytes([b for b in data if 32 <= b <= 127])
                if filtered_data:
                    try:
                        decoded_data = filtered_data.decode('utf-8').strip()
                        print(f"Dades decodificades: {decoded_data}")
                    except UnicodeDecodeError as e:
                        print(f"Error de decodificació: {e}")
            except Exception as e:
                print(f"Error en manejar les dades: {e}")
        else:
            # Mostra un missatge si no hi ha dades
            print("Esperant dades...")
        time.sleep(2)  # Temps d'espera ajustat per evitar saturacions
except KeyboardInterrupt:
    print("Interromput per l'usuari.")
    ser.close()
