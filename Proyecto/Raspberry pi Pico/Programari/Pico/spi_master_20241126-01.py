import spidev
import time
import json

# Configurar SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus SPI 0, dispositiu 0
spi.max_speed_hz = 50000
spi.mode = 0

def enviar_rebre_dades(data_dict):
    try:
        # Convertir diccionari a JSON i després a bytes
        data_bytes = json.dumps(data_dict).encode('utf-8')
        data_to_send = list(data_bytes[:64])  # Limitar a 64 bytes
        while len(data_to_send) < 64:  # Completar amb zeros
            data_to_send.append(0)

        print(f"Dades a enviar: {data_dict}")
        response = spi.xfer(data_to_send)  # Enviar i rebre dades
        print(f"Resposta crua de la Pico: {response}")

        # Convertir resposta a cadena
        response_str = ''.join([chr(byte) for byte in response if byte != 0])
        if response_str:
            response_dict = json.loads(response_str)
            print(f"Resposta de la Pico (com a diccionari): {response_dict}")
        else:
            print("Resposta de la Pico buida o no vàlida.")

    except Exception as e:
        print(f"Error durant la comunicació: {e}")

# Prova periòdica
while True:
    dades = {"temperatura": 25, "humitat": 60, "estat": "OK"}
    enviar_rebre_dades(dades)
    time.sleep(1)
