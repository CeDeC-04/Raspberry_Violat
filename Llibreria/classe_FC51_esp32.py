from machine import Pin
import time

class SensorInfrarrojo:
    def __init__(self, pin, platform):
        """Constructor del objeto"""
        self.pin = pin
        self.platform = platform
        
        self.pin = Pin(self.pin, Pin.IN) 

    def detecta_obstacle(self):
        """Retorna True si detecta un obstáculo, False en caso contrario."""
        if self.pin.value() == 0:
            return True
        return False