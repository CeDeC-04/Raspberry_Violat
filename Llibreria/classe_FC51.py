import importlib
import time

class SensorInfrarrojo:
    def __init__(self, pin, platform):
        """Constructor del objeto"""
        self.pin = pin
        self.platform = platform

        if self.platform == "pi_3":
            self.GPIO = importlib.import_module('RPi.GPIO')
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setup(self.pin, self.GPIO.IN)
        
        elif self.platform == "pi_pico":
            self.GPIO = importlib.import_module('machine')
            self.pin = self.GPIO.Pin(self.pin, self.GPIO.IN) 

    def detecta_obstacle(self):
        """Retorna True si detecta un obstáculo, False en caso contrario."""
        if self.platform == "pi_3":
            if self.GPIO.input(self.pin) == self.GPIO.LOW:
                return True
        elif self.platform == "pi_pico":
            if self.pin.value() == 0:
                return True
        return False

    def cleanup(self):
        """Limpia la configuración de GPIO."""
        if self.platform == "pi_3":
            self.GPIO.cleanup()