import sys
import platform

class WIFI:
    def __init__(self):
        self.moduls_carregats = {}
        self._detectar_placa()
        self._importar_moduls()

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
            moduls_necessaris = ["esp", "network", "utime"]
        else:
            raise EnvironmentError("Cap mòdul disponible per a aquesta placa.")

        for modul in moduls_necessaris:
            try:
                self.moduls_carregats[modul] = __import__(modul)
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

# Exemple d'ús
wifi = WIFI()
print(f"Placa detectada: {wifi.info()['placa']}")
print(f"Mòduls carregats: {wifi.info()['moduls_carregats']}")
