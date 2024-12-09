import importlib
import time

class Buzzer_Actiu:
    def __init__(self, buzzer_pin, platform):
        """Constructor del objeto"""
        self.pin = buzzer_pin
        self.platform = platform

        if self.platform == "pi_3":
            self.GPIO = importlib.import_module('RPi.GPIO')
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setup(self.pin, self.GPIO.OUT) 
        
        elif self.platform == "pi_pico":
            self.GPIO = importlib.import_module('machine')
            self.pin = self.GPIO.Pin(self.pin, self.GPIO.OUT)

    def encen(self):
        """Activa el buzzer (sonido)."""
        if self.platform == "pi_3":
            self.GPIO.output(self.pin, self.GPIO.HIGH)
        elif self.platform == "pi_pico":
            self.pin.value(1)

    def apaga(self):
        """Desactiva el buzzer (sin sonido)."""
        if self.platform == "pi_3":
            self.GPIO.output(self.pin, self.GPIO.LOW)
        elif self.platform == "pi_pico":
            self.pin.value(0)

    def sonar_durant(self, segons):
        """Hace sonar el buzzer durante un tiempo determinado (en segundos)."""
        self.encen()
        time.sleep(segons)
        self.apaga()

    def cleanup(self):
        """Limpia la configuración de GPIO."""
        if self.platform == "pi_3":
            self.GPIO.cleanup()  # Limpia la configuración en Raspberry Pi 3