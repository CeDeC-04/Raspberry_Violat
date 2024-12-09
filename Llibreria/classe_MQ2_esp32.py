from machine import Pin
import time

class MQ2:
    def __init__(self, pin, platform):
        """Constructor del Objeto"""
        self.pin = pin
        self.platform = platform

        self.pin = Pin(self.pin, Pin.IN)  # En la Pico, la configuración es diferente

    def detecta_particules(self):
        """Retorna True si detecta partículas, False en caso contrario."""
        if self.pin.value() == 0:  # MicroPython usa 0 o 1 para los pines digitales
            return True
        return False