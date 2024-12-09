'''
Arxiu anterior: 
    1- main_WIFI_BetaPasaPas_20241208.py
'''
import network
import socket
import time


class WIFI:
    def __init__(self, raspberry_ip = '192.168.4.2', raspberry_port = 12346, esp32_ip = '192.168.4.1', esp32_port = 12345):

        # Sortides comprovació estat WIFI
        self.actiu, self.conectat, self.comunicant = False, False, False
        
        # Configura l'ESP32 com a punt d'accés
        self.ssid = 'ESP32_AP'
        self.password = '12345678'
                
        self.actiu = True
        
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=self.ssid, password=self.password, authmode=network.AUTH_WPA_WPA2_PSK)

        #print("Punt d'accés actiu")
        #print("SSID:", ssid)
        #print("IP:", ap.ifconfig()[0])  # Mostra la IP del punt d'accés
        
        # Configura el servidor TCP de l'ESP32
        
        self.esp32_ip = esp32_ip 
        self.esp32_port = esp32_port
                
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.esp32_ip, self.esp32_port))  # IP del punt d'accés i port
        self.server_socket.listen(1)

        #print("Servidor TCP actiu a 192.168.4.1:12345")

        # IP de la Raspberry Pi dins de la xarxa ESP32_AP
        self.raspberry_ip = raspberry_ip
        self.raspberry_port = raspberry_port  # Port del servidor TCP de la Raspberry Pi
        
        self.conectat = True

    
    def WIFI_comunicacio(self, envia_missatge = ''):
        """ Com a servidor: escolta i rep missatges de la Raspberry Pi """
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
                self.comunicant = False
            else:
                self.comunicant = True

            data = conn.recv(1024).decode('utf-8')
            conn.close()

            # Com a client: envia missatges a la Raspberry Pi
            client_socket = self.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.raspberry_ip, self.raspberry_port))

            client_socket.send(envia_missatge.encode('utf-8'))
    # BORRAR
            print(f"Missatge enviat a la Raspberry Pi: {message}")

            client_socket.close()

            '''
            if self.comunicant:
                # Rep el missatge
                data = conn.recv(1024).decode('utf-8')
                conn.close()

                # Com a client: envia missatges a la Raspberry Pi

                #client_socket = self.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.raspberry_ip, self.raspberry_port))

                client_socket.send(envia_missatge.encode('utf-8'))
    # BORRAR
                print(f"Missatge enviat a la Raspberry Pi: {message}")

                client_socket.close()
            '''

            self.comunicant = False
            return(data)
                
        except Exception as e:
            return None
       
        
 
        
    def WIFI_comprovacio(self):
        '''Prova de comunicació entre Pi3 i ESP32, només cridar aquest metode de l'objecte'''
        try:
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
        except KeyboardInterrupt:
            print("Aturada manual per l'usuari")



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
