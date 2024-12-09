import importlib
import time

class MQ2:
    def __init__(self, pin, platform):
        """Constructor del Objeto"""
        self.pin = pin
        self.platform = platform
        
        if self.platform == "pi_3":
            self.GPIO = importlib.import_module('RPi.GPIO')
        elif self.platform == "pi_pico":
            self.GPIO = importlib.import_module('machine')

        # Configuración de los pines
        if self.platform == "pi_3":
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setup(self.pin, self.GPIO.IN)
        elif self.platform == "pi_pico":
            self.pin = self.GPIO.Pin(self.pin, self.GPIO.IN)  # En la Pico, la configuración es diferente

    def detecta_particules(self):
        """Retorna True si detecta partículas, False en caso contrario."""
        if self.platform == "pi_3":
            if self.GPIO.input(self.pin) == self.GPIO.LOW:
                return True
        elif self.platform == "pi_pico":
            if self.pin.value() == 0:  # MicroPython usa 0 o 1 para los pines digitales
                return True
        return False

    def cleanup(self):
        """Limpia la configuración de GPIO."""
        if self.platform == "pi_3":
            self.GPIO.cleanup()