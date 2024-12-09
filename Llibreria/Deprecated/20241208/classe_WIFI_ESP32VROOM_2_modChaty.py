import sys
import platform
import network
import socket
import time

class WIFI:
    def __init__(self, raspberry_ip = '0.0.0.0', raspberry_port = 12346, esp32_ip = '192.168.4.1', esp32_port = 12345):

        # Sortides comprovació estat WIFI
        self.actiu, self.conectat, self.comunicant = False, False, False

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
        self.esp32_ip = esp32_ip
        self.esp32_port = esp32_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.esp32_ip, self.esp32_port))  # IP del punt d'accés i port
        self.server_socket.listen(1)
            
        print(f"Servidor TCP actiu a {self.esp32_ip}:{self.esp32_port}")
            
        # IP de la Raspberry Pi dins de la xarxa ESP32_AP
        self.raspberry_ip = '192.168.4.2'
        self.raspberry_port = raspberry_port  # Port del servidor TCP de la Raspberry Pi


    def WIFI_reinicia(self, espera = 1):
        """
        Reinicia el component WIFI de la placa.
        Només implementat per Raspberry Pi3
        """
        self.WIFI_desconecta(espera)
        self.actiu, self.conectat, self.comunicant = False, False, False
        self.WIFI_scan(espera * 1)
        self.actiu = True
        self.WIFI_conecta(espera * 3)
        self.conectat = True

    def WIFI_desconecta(self, espera = 1):
        """
        Desconnecta el component WIFI de la placa.
        Només implementat per Raspberry Pi3
        """
        if self.placa == "PI3":
            os.system("sudo nmcli dev disconnect wlan0")
            time.sleep(espera)

    def WIFI_scan(self, espera = 1):
        """
        Escaneja les SCID WIFI disponibles.
        Només implementat per Raspberry Pi3
        """
        os.system("sudo nmcli dev wifi rescan")
        time.sleep(espera)

    def WIFI_conecta(self, espera = 3):
        """
        Es conecta a la SCID WIFI  del ESP32.
        Només implementat per Raspberry Pi3
        """
        os.system("sudo nmcli dev wifi connect ESP32_AP password 12345678")
        time.sleep(espera)

    def WIFI_comunicacio(self, envia_missatge = ''):
        while True:
            try:
                # Estableix un temps d'espera manual per la connexió
                start_time = time.time()
                conn = None
                while (time.time() - start_time) < 10:  # Temps màxim d'espera: 10 segons
                    try:
                        conn, addr = self.server_socket.accept()
                        break
                    except OSError as e:
                        pass  # Cap connexió encara

                if conn is None:
                    print("Timeout esperant connexió.")
                    continue
                
                # Rep el missatge
                data = conn.recv(1024).decode('utf-8')
               
                conn.close()
                
                # Com a client: envia missatges a la Raspberry Pi
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.raspberry_ip, self.raspberry_port))
                client_socket.send(envia_missatge.encode('utf-8'))

                client_socket.close()
                
                return (data)
                    
            except Exception as e:
                print(f"Error: {e}")

    def WIFI_comprovacio(self):
        while True:
            try:
                # Com a servidor: escolta i rep missatges de la Raspberry Pi
                print("Esperant connexió de la Raspberry Pi...")

                # Estableix un temps d'espera manual per la connexió
                start_time = time.time()
                conn = None
                while (time.time() - start_time) < 10:  # Temps màxim d'espera: 10 segons
                    try:
                        conn, addr = self.server_socket.accept()
                        break
                    except OSError as e:
                        pass  # Cap connexió encara

                if conn is None:
                    print("Timeout esperant connexió.")
                    continue

                print(f"Connexió establerta amb: {addr}")
                
                # Rep el missatge
                data = conn.recv(1024).decode('utf-8')
                print(f"Missatge rebut: {data}")
                
                conn.close()
            except Exception as e:
                print(f"Error: {e}")
