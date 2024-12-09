import importlib
import time

class Rele:
    def __init__(self, pin, platform):
        """Constructor del Objeto"""
        self.pin = pin
        self.platform = platform
        
        if self.platform == "pi_3":
            self.GPIO = importlib.import_module('RPi.GPIO')
        elif self.platform == "pi_pico":
            self.GPIO = importlib.import_module('machine')

        # Importar la librería adecuada según el tipo de plataforma
        if self.platform == "pi_3":
            self.GPIO = importlib.import_module('RPi.GPIO')
        elif self.platform == "pi_pico":
            self.GPIO = importlib.import_module('machine')

        # Configuración de los pines
        if self.platform == "pi_3":
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setup(self.pin, self.GPIO.OUT)
        elif self.platform == "pi_pico":
            self.pin = self.GPIO.Pin(self.pin, self.GPIO.OUT)

        self.state = False

    def encen(self):
        """Encén el Rele."""
        if self.platform == "pi_3":
            self.GPIO.output(self.pin, self.GPIO.HIGH)
        elif self.platform == "pi_pico":
            self.pin.value(1)
        self.state = True

    def apaga(self):
        """Apaga el Rele."""
        if self.platform == "pi_3":
            self.GPIO.output(self.pin, self.GPIO.LOW)
        elif self.platform == "pi_pico":
            self.pin.value(0)
        self.state = False

    def alterna(self):
        """Canvia l'estat del Rele."""
        if self.state:
            self.apaga()
        else:
            self.encen()

    def cleanup(self):
        """Neteja la configuració de GPIO."""
        if self.platform == "pi_3":
            self.GPIO.cleanup()