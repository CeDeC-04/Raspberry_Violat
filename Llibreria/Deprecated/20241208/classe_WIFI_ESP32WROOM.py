import network
import socket
import time

class WIFI(): #ESP32NetworkManager:
    def __init__(self, raspberry_ip = '0.0.0.0', raspberry_port = 12346, esp32_ip = '192.168.4.1', esp32_port = 12345):
        self.ssid = 'ESP32_AP'
        self.password = '12345678'
        self.raspberry_ip = '0.0.0.0'
        self.raspberry_port = 12346  # Port del servidor de la Raspberry Pi
        self.esp32_ip = esp32_ip      # Ip del ESP32
        self.esp32_port = esp32_port  # Port del servidor TCP de l'ESP32
        self.ap = None
        self.server_socket = None

    def configure_access_point(self):
        try:
            self.ap = network.WLAN(network.AP_IF)
            self.ap.active(True)
            self.ap.config(essid=self.ssid, password=self.password, authmode=network.AUTH_WPA_WPA2_PSK)
            #print("Punt d'accés actiu")
            #print("SSID:", self.ssid)
            #print("IP:", self.ap.ifconfig()[0])
            return(True)
        except:
            return(False)
        
    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(1)
            return(True)#print(f"Servidor TCP actiu a {self.server_ip}:{self.server_port}")
        except:
            return(False)
        
    def wait_for_connection(self, timeout=10):
        #print("Esperant connexió de la Raspberry Pi...")
        start_time = time.time()
        conn = None
        while (time.time() - start_time) < timeout:
            try:
                conn, addr = self.server_socket.accept()
                #print(f"Connexió establerta amb: {addr}")
                return conn
            except OSError:
                pass
        print("Timeout esperant connexió.")
        return None

    def receive_message(self, conn):
        data = conn.recv(1024).decode('utf-8')
        #print(f"Missatge rebut de la Raspberry Pi: {data}")
        conn.close()
        return(data)

    def send_message_to_client(self, message_to_send = ''):
        #print("Connectant com a client al servidor de la Raspberry Pi...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.client_ip, self.client_port))
            client_socket.send(message_to_send.encode('utf-8'))
            #print(f"Missatge enviat a la Raspberry Pi: {message}")
        except:
            return(False)
        finally:
            client_socket.close()
            return(True)

    def run(self, message_to_send = ''):
        #print(message_to_send)
        #self.configure_access_point()
        #self.start_server()
        try:
            conn = self.wait_for_connection()
            if conn:
                data = self.receive_message(conn)
                self.send_message_to_client(message_to_send)
                return(data)
        except Exception as e:
            return(f"Error: {e}")
