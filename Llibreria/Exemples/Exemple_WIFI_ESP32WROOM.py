from clase_wifi_xgpt import * 
# Exemple d'ús de la classe ESP32NetworkManager
if __name__ == "__main__":
    esp32_manager = ESP32NetworkManager(
        ssid='ESP32_AP',
        password='12345678',
        server_ip='192.168.4.1',
        server_port=12345,
        client_ip='192.168.4.2',
        client_port=12346
    )
    print(esp32_manager.run("Felicitats Joan"))

esp32_manager.configure_access_point()
esp32_manager.start_server()
missatge = "Felicitats Joan"
while True:
    missatge += "!"
    try:
        print(esp32_manager.run(missatge))
    except Exception as e:
        print(f"Error: {e}")