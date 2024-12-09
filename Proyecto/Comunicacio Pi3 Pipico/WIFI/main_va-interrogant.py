import network
import socket

# Configura l'ESP32 com a punt d'accés
ssid = 'ESP32_AP'
password = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)

print("Punt d'accés actiu")
print("SSID:", ssid)
print("IP:", ap.ifconfig()[0])  # Normalment serà 192.168.4.1

# Configura el servidor per enviar dades a la Raspberry Pi
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.4.1', 12345))  # IP de l'ESP32 i port
server_socket.listen(1)

print("Esperant connexions...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connexió establerta amb: {addr}")
    
    # Envia un missatge a la Raspberry Pi
    message = "Hola Raspberry"
    conn.send(message.encode('utf-8'))
    print(f"Missatge enviat: {message}")
    
    conn.close()
