from machine import Pin
import time

class Rele:
    def __init__(self, pin, platform):
        """Constructor del Objeto"""
        self.pin = pin
        self.platform = platform

        self.pin = Pin(self.pin, Pin.OUT)

        self.state = False

    def encen(self):
        """Encén el Rele."""
        self.pin.value(1)
        self.state = True

    def apaga(self):
        """Apaga el Rele."""
        self.pin.value(0)
        self.state = False

    def alterna(self):
        """Canvia l'estat del Rele."""
        if self.state:
            self.apaga()
        else:
            self.encen()