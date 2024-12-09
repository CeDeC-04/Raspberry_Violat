'''
Arxiu anterior: 
    1-raspberry_bireccional_WIFI_20241129_BetaPasaPas_20241208.py
'''
import socket
import time
from classe_WIFI_RaspPI3_Beta import *
'''
# Configura el servidor TCP de la Raspberry Pi
raspberry_ip = '0.0.0.0'
raspberry_port = 12346  # Port del servidor de la Raspberry Pi

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((raspberry_ip, raspberry_port))
server_socket.listen(1)

print(f"Servidor TCP actiu a {raspberry_ip}:{raspberry_port}")

# IP de l'ESP32 dins de la xarxa ESP32_AP
esp_ip = '192.168.4.1'
esp_port = 12345  # Port del servidor TCP de l'ESP32
'''
                
                ###### MAIN ######    

COMs = WIFI()

missatge = "hola"

while True:
    try:
        
               
        # Envia i rep el missateg de l'ESP32
        print(COMs.WIFI_comunicacio(missatge))
        
        missatge += "a"
        time.sleep(1)  # Espera 5 segons abans del següent cicle

    except socket.timeout:
        print("Timeout esperant connexió.")
    except KeyboardInterrupt:
        #print("Inici aturat per l'usuari")
        #COMs.WIFI_tanca()
        #COMs.WIFI_desconecta()
        #COMs.WIFI_scan()
        print("Aturat per l'usuari")
    except Exception as e:
        print(f"Error: {e}")



'''         
                

while True:
    try:
        # Com a client: envia missatges a l'ESP32
        print("Connectant com a client al servidor de l'ESP32...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((esp_ip, esp_port))

        message = "Hola ESP"
        client_socket.send(message.encode('utf-8'))
        print(f"Missatge enviat a l'ESP32: {message}")

        client_socket.close()

        # Com a servidor: escolta i rep missatges de l'ESP32
        print("Esperant connexió de l'ESP32...")
        server_socket.settimeout(10)  # Timeout per no bloquejar indefinidament
        conn, addr = server_socket.accept()
        print(f"Connexió establerta amb: {addr}")

        # Rep el missatge
        data = conn.recv(1024).decode('utf-8')
        print(f"Missatge rebut de l'ESP32: {data}")

        conn.close()

        time.sleep(1)  # Espera 5 segons abans del següent cicle

    except socket.timeout:
        print("Timeout esperant connexió.")
    except Exception as e:
        print(f"Error: {e}")
        
        
'''