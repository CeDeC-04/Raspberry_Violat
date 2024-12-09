import RPi.GPIO as GPIO
import time

class Rele:
    def __init__(self, pin, platform):
        """Constructor del Objeto"""
        self.pin = pin
        self.platform = platform

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.state = False

    def encen(self):
        """Encén el Rele."""
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True

    def apaga(self):
        """Apaga el Rele."""
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def alterna(self):
        """Canvia l'estat del Rele."""
        if self.state:
            self.apaga()
        else:
            self.encen()

    def cleanup(self):
        """Neteja la configuració de GPIO."""
        GPIO.cleanup()