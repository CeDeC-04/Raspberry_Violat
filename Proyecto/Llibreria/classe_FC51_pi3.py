import RPi.GPIO as GPIO
import time

class SensorInfrarrojo:
    def __init__(self, pin, platform):
        """Constructor del objeto"""
        self.pin = pin
        self.platform = platform

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def detecta_obstacle(self):
        """Retorna True si detecta un obstáculo, False en caso contrario."""
        if GPIO.input(self.pin) == GPIO.LOW:
            return True
        return False

    def cleanup(self):
        """Limpia la configuración de GPIO."""
        GPIO.cleanup()