'''
import socket
import time
import os
'''

import sys
import platform

class WIFI:
    def __init__(self, raspberry_ip = '0.0.0.0', raspberry_port = 12346, esp32_ip = '192.168.4.1', esp32_port = 12345):
        self.moduls_carregats = {}
        self._detectar_placa()
        self._importar_moduls()

        #######

        # Sortides comprovació estat WIFI
        self.actiu, self.conectat, self.comunicant = False, False, False
        
        # Configura el servidor TCP de la Raspberry Pi
        self.raspberry_ip = '0.0.0.0'
        self.raspberry_port = 12346  # Port del servidor de la Raspberry Pi

        self.actiu = True

        socket = self.moduls_carregats["socket"]
        #os = self.moduls_carregats["os"]
        #time = self.moduls_carregats["time"]
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((raspberry_ip, raspberry_port))
        self.server_socket.listen(1)

        # IP de l'ESP32 dins de la xarxa ESP32_AP
        self.esp32_ip = esp32_ip      # Ip del ESP32
        self.esp32_port = esp32_port  # Port del servidor TCP de l'ESP32

        self.conectat = True
        
        self.reiniciWIFI = 0


    def _detectar_placa(self):
        """
        Detecta si estem executant a Raspberry Pi 3 o ESP32.
        """
        if "linux" in sys.platform and "arm" in platform.machine():
            self.placa = "PI3"
        elif "esp32" in sys.platform:
            self.placa = "ESP32"
        else:
            raise EnvironmentError("Placa desconeguda o no suportada.")

    def _importar_moduls(self):
        """
        Carrega els mòduls necessaris segons la placa detectada.
        """
        if self.placa == "PI3":
            moduls_necessaris = ["socket", "time", "os"]
        elif self.placa == "ESP32":
            moduls_necessaris = ["network", "socket", "time"]
        else:
            raise EnvironmentError("Cap mòdul disponible per a aquesta placa.")

        for modul in moduls_necessaris:
            try:
                self.moduls_carregats[modul] = __import__(modul)
                sys.modules[modul] = modul
                
                
                globals()[modul] = self.moduls_carregats[modul]
                https://chatgpt.com/c/674cc705-a7d8-800e-8f5e-93984ad186d8
                
                
            except ImportError:
                print(f"Error: No s'ha pogut importar el mòdul {modul}")

    def info(self):
        """
        Retorna informació sobre la configuració de la placa.
        """
        return {
            "placa": self.placa,
            "moduls_carregats": list(self.moduls_carregats.keys())
        }

        
    def WIFI_reinicia(self, espera = 1):
        """
        Reinicia el component WIFI de la placa.
        Només implementat per Raspberry Pi3
        """
        if self.placa == "PI3":
            self.WIFI_desconecta(espera)
            self.actiu, self.conectat, self.comunicant = False, False, False
            self.WIFI_scan(espera * 1)
            self.actiu = True
            self.WIFI_conecta(espera * 3)
            self.conectat = True
        '''else:
            return ("Només implementat per PI3")
        '''
 
    def WIFI_desconecta(self, espera = 1):
        """
        Desconnecta el component WIFI de la placa.
        Només implementat per Raspberry Pi3
        """
        if self.placa == "PI3":
            os = self.moduls_carregats["os"] # Crida al modul que s'ha creat internament encapsulat
            time = self.moduls_carregats["time"] # Crida al modul que s'ha creat internament encapsulat

            os.system("sudo nmcli dev disconnect wlan0")
            time.sleep(espera)
        '''        else:
            return ("Només implementat per PI3")
        '''  

    def WIFI_scan(self, espera = 1):
        """
        Escaneja les SCID WIFI disponibles.
        Només implementat per Raspberry Pi3
        """
        if self.placa == "PI3":
            os = self.moduls_carregats["os"] # Crida al modul que s'ha creat internament encapsulat
            time = self.moduls_carregats["time"] # Crida al modul que s'ha creat internament encapsulat
            
            os.system("sudo nmcli dev wifi rescan")
            time.sleep(espera)
        '''        else:
            return ("Només implementat per PI3")
        '''  

    def WIFI_conecta(self, espera = 3):
        """
        Es conecta a la SCID WIFI  del ESP32.
        Només implementat per Raspberry Pi3
        """

        if self.placa == "PI3":
            os = self.moduls_carregats["os"] # Crida al modul que s'ha creat internament encapsulat
            time = self.moduls_carregats["time"] # Crida al modul que s'ha creat internament encapsulat
            
            os.system("sudo nmcli dev wifi connect ESP32_AP password 12345678")
            time.sleep(espera)
        else:
            return ("Només implementat per PI3")


    def WIFI_comunicacio(self, envia_missatge = ''):
        
        if self.placa == "PI3":
            socket = self.moduls_carregats["socket"] # Crida al modul que s'ha creat internament encapsulat
            try:
                self.comunicant = True
                # Com a client: envia missatges a l'ESP32
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.esp32_ip, self.esp32_port))
                client_socket.send(envia_missatge.encode('utf-8'))
                client_socket.close()
                
                # Com a servidor: escolta i rep missatges de l'ESP32
                self.server_socket.settimeout(10)  # Timeout per no bloquejar indefinidament
                conn, addr = self.server_socket.accept()
                
                # Rep el missatge
                data = conn.recv(1024).decode('utf-8')
                conn.close()
                
                self.comunicant = False
                return(data)
                
            except socket.timeout:
                print("Timeout esperant connexió.")
            except Exception as e:
                print(f"Error: {e}")

        
    def WIFI_comprovacio(self):
    
        if self.placa == "PI3":
            time = self.moduls_carregats["time"] # Crida al modul que s'ha creat internament encapsulat
            socket = self.moduls_carregats["socket"] # Crida al modul que s'ha creat internament encapsulat
            while True:
                try:
                    # Com a client: envia missatges a l'ESP32
                    print("Connectant com a client al servidor de l'ESP32...")
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((self.esp32_ip, self.esp32_port))
                    
                    message = "Hola ESP"
                    client_socket.send(message.encode('utf-8'))
                    print(f"Missatge enviat a l'ESP32: {message}")
                    
                    client_socket.close()
                    
                    # Com a servidor: escolta i rep missatges de l'ESP32
                    print("Esperant connexió de l'ESP32...")
                    self.server_socket.settimeout(10)  # Timeout per no bloquejar indefinidament
                    conn, addr = self.server_socket.accept()
                    print(f"Connexió establerta amb: {addr}")
                    
                    # Rep el missatge
                    data = conn.recv(1024).decode('utf-8')
                    print(f"Missatge rebut de l'ESP32: {data}")
                    
                    conn.close()
                    
                    time.sleep(1)  # Espera x segons abans del següent cicle
                    
                    print(reiniciWIFI)
                    reiniciWIFI += 1
                    
                    if reiniciWIFI > 5:
                        wifi.WIFI_reinicia()
                        reiniciWIFI = -1
                        
                except socket.timeout:
                    print("Timeout esperant connexió.")
                except Exception as e:
                    print(f"Error: {e}")


'''
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

        # Estableix un temps d'espera manual per la connexió
        start_time = time.time()
        conn = None
        while (time.time() - start_time) < 10:  # Temps màxim d'espera: 10 segons
            try:
                conn, addr = server_socket.accept()
                break
            except OSError as e:
                pass  # Cap connexió encara

        if conn is None:
            print("Timeout esperant connexió.")
            continue

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

        time.sleep(1)  # Espera 5 segons abans del següent cicle

    except Exception as e:
        print(f"Error: {e}")
'''