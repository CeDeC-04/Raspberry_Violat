import network
import socket
import time

class ESP32NetworkManager:
    def __init__(self, ssid, password, server_ip, server_port, client_ip, client_port):
        self.ssid = ssid
        self.password = password
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_ip = client_ip
        self.client_port = client_port
        self.ap = None
        self.server_socket = None

    def configure_access_point(self):
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=self.ssid, password=self.password, authmode=network.AUTH_WPA_WPA2_PSK)
        print("Punt d'accés actiu")
        print("SSID:", self.ssid)
        print("IP:", self.ap.ifconfig()[0])

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(1)
        print(f"Servidor TCP actiu a {self.server_ip}:{self.server_port}")

    def wait_for_connection(self, timeout=10):
        print("Esperant connexió de la Raspberry Pi...")
        start_time = time.time()
        conn = None
        while (time.time() - start_time) < timeout:
            try:
                conn, addr = self.server_socket.accept()
                print(f"Connexió establerta amb: {addr}")
                return conn
            except OSError:
                pass
        print("Timeout esperant connexió.")
        return None

    def receive_message(self, conn):
        data = conn.recv(1024).decode('utf-8')
        print(f"Missatge rebut de la Raspberry Pi: {data}")
        conn.close()

    def send_message_to_client(self, message):
        print("Connectant com a client al servidor de la Raspberry Pi...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.client_ip, self.client_port))
            client_socket.send(message.encode('utf-8'))
            print(f"Missatge enviat a la Raspberry Pi: {message}")
        finally:
            client_socket.close()

    def run(self):
        self.configure_access_point()
        self.start_server()
        while True:
            try:
                conn = self.wait_for_connection()
                if conn:
                    self.receive_message(conn)
                    self.send_message_to_client("Hola Raspberry")
                time.sleep(1)  # Espera 1 segon abans del següent cicle
            except Exception as e:
                print(f"Error: {e}")
