import network
import socket
import time

# Configura l'ESP32 com a punt d'accés
ssid = 'ESP32_AP'
password = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)

print("Punt d'accés actiu")
print("SSID:", ssid)
print("IP:", ap.ifconfig()[0])  # Mostra la IP del punt d'accés

# Configura el servidor TCP de l'ESP32
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.4.1', 12345))  # IP del punt d'accés i port
server_socket.listen(1)

print("Servidor TCP actiu a 192.168.4.1:12345")

# IP de la Raspberry Pi dins de la xarxa ESP32_AP
raspberry_ip = '192.168.4.2'
raspberry_port = 12346  # Port del servidor TCP de la Raspberry Pi

while True:
    try:
        # Com a servidor: escolta i rep missatges de la Raspberry Pi
        print("Esperant connexió de la Raspberry Pi...")
        server_socket.settimeout(10)  # Timeout per no bloquejar indefinidament
        conn, addr = server_socket.accept()
        print(f"Connexió establerta amb: {addr}")

        # Rep el missatge
        data = conn.recv(1024).decode('utf-8')
        print(f"Missatge rebut de la Raspberry Pi: {data}")

        conn.close()

        # Com a client: envia missatges a la Raspberry Pi
        print("Connectant com a client al servidor de la Raspberry Pi...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((raspberry_ip, raspberry_port))

        message = "Hola Raspberry"
        client_socket.send(message.encode('utf-8'))
        print(f"Missatge enviat a la Raspberry Pi: {message}")

        client_socket.close()

        time.sleep(5)  # Espera 5 segons abans del següent cicle

    except socket.timeout:
        print("Timeout esperant connexió.")
    except Exception as e:
        print(f"Error: {e}")

