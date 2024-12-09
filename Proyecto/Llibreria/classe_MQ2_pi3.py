import RPi.GPIO as GPIO
import time

class MQ2:
    def __init__(self, pin, platform):
        """Constructor del Objeto"""
        self.pin = pin
        self.platform = platform
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def detecta_particules(self):
        """Retorna True si detecta partículas, False en caso contrario."""
        if self.GPIO.input(self.pin) == self.GPIO.LOW:
            return True
        return False

    def cleanup(self):
        """Limpia la configuración de GPIO."""
        GPIO.cleanup()