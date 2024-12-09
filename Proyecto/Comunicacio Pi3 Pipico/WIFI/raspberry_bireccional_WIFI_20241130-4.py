import socket
import time
import os


class WIFI():
    
    def __init__(self, raspberry_ip = '0.0.0.0', raspberry_port = 12346, esp32_ip = '192.168.4.1', esp32_port = 12345):
        # Configura el servidor TCP de la Raspberry Pi
        self.raspberry_ip = '0.0.0.0'
        self.raspberry_port = 12346  # Port del servidor de la Raspberry Pi

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((raspberry_ip, raspberry_port))
        self.server_socket.listen(1)

        # IP de l'ESP32 dins de la xarxa ESP32_AP
        self.esp32_ip = esp32_ip      # Ip del ESP32
        self.esp32_port = esp32_port  # Port del servidor TCP de l'ESP32

        self.reiniciWIFI = 0
        
        
    def WIFI_reinicia(self, espera = 1):
        self.WIFI_desconecta(espera)
        self.WIFI_scan(espera * 1)
        self.WIFI_conecta(espera * 3)
    
    
    def WIFI_desconecta(self, espera = 1):
        os.system("sudo nmcli dev disconnect wlan0")
        time.sleep(espera)
    
    def WIFI_scan(self, espera = 1):
        os.system("sudo nmcli dev wifi rescan")
        time.sleep(espera)
    
    def WIFI_conecta(self, espera = 3):
        os.system("sudo nmcli dev wifi connect ESP32_AP password 12345678")
        time.sleep(espera)

        
    def WIFI_comprovacio(self):
    
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

                time.sleep(1)  # Espera 5 segons abans del següent cicle
        
                print(reiniciWIFI)
                reiniciWIFI += 1
        
                if reiniciWIFI > 5:
                    wifi.WIFI_reinicia()

                    reiniciWIFI = -1

            except socket.timeout:
                print("Timeout esperant connexió.")
            except Exception as e:
                print(f"Error: {e}")



            # Fer l'Script per a reiniciar la WIFI si es bloquejar
            '''
            sudo nmcli dev disconnect wlan0
                Device 'wlan0' successfully disconnected.
            sudo nmcli dev wifi rescan
            sudo nmcli dev wifi connect ESP32_AP password 12345678
                Device 'wlan0' successfully activated with 'c6e86c1b-0b45-4a49-851e-5f42dd9bb5cd'.
            '''

    def WIFI_comunicacio(self, envia_missatge = ''):
    
        try:
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
            return(data)
        except socket.timeout:
            print("Timeout esperant connexió.")
        except Exception as e:
            print(f"Error: {e}")

wifi = WIFI()

wifi.WIFI_reinicia()

envia = "Juanfri, espavila!! \n\nxDDDDDDDDDD"


try:
    while True:
        print(wifi.WIFI_comunicacio(envia))
except KeyboardInterrupt:
    print(f"Interromput per l'usiari")

