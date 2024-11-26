from machine import Pin, SPI
import time
import json

# Configurar SPI com a esclau
spi = SPI(0, baudrate=50000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
cs = Pin(17, Pin.IN, Pin.PULL_UP)  # Pin de selecció de dispositiu (CS)

# Funció per processar les dades
def procesar_dades():
    if not cs.value():  # Comprova si el pin de selecció (CS) està actiu
        
        print("CS activat, llegint dades...")
        
        message = spi.read(64)  # Llegir fins a 64 bytes des del master
        print("Dades llegides:", message)
        
        # Imprimir els bytes rebuts per veure si s'estan enviant correctament
        print("Dades en brut:", message)

        # Convertir els bytes a cadena
        try:
            message_str = message.decode('utf-8')
            print("Missatge rebut:", message_str)

            # Convertir la cadena JSON en un diccionari
            data_dict = json.loads(message_str)
            print("Diccionari rebut:", data_dict)

            # Resposta dinàmica basada en el diccionari rebut
            if "temperatura" in data_dict:
                resposta = {"temperatura_rebuda": data_dict["temperatura"] + 1}  # Exemple: incrementar la temperatura rebuda
            else:
                resposta = {"error": "Dades no vàlides"}  # Resposta per error

            # Convertir el diccionari de resposta a JSON i després a bytes
            resposta_bytes = json.dumps(resposta).encode('utf-8')
            spi.write(resposta_bytes)  # Enviar la resposta al master
            print("Resposta enviada:", resposta_bytes)

        except ValueError:
            print("Error en la conversió del JSON")
        
while True:
    procesar_dades()
    time.sleep(0.1)
