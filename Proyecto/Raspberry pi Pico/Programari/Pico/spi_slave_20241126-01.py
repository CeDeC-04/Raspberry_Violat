from machine import Pin, SPI
import json

# Configurar SPI com a esclau
spi = SPI(0, baudrate=50000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
cs = Pin(17, Pin.IN, Pin.PULL_UP)  # Pin de selecció de dispositiu (CS)

def procesar_dades():
    try:
        if not cs.value():  # Si CS està actiu
            # Llegir dades del Master
            message = spi.read(64)  # Llegir fins a 64 bytes
            print(f"Dades rebudes crues: {message}")

            # Convertir bytes a JSON
            message_str = ''.join([chr(b) for b in message if b != 0])
            print(f"Missatge rebut com a text: {message_str}")
            if message_str:
                data_dict = json.loads(message_str)
                print(f"Diccionari rebut: {data_dict}")

                # Preparar resposta
                response = json.dumps({"estat": "rebut"}).encode('utf-8')
                response_bytes = list(response[:64])
                while len(response_bytes) < 64:  # Completar amb zeros
                    response_bytes.append(0)
                spi.write(bytearray(response_bytes))
                print("Resposta enviada al Master.")

    except Exception as e:
        print(f"Error durant la recepció: {e}")

# Bucle principal
while True:
    procesar_dades()
