import importlib
import time

class SensorPIR:
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

    def detecta_moviment(self):
        """Retorna True si detecta movimiento, False en caso contrario."""
        if self.platform == "pi_3":
            if self.GPIO.input(self.pin) == self.GPIO.HIGH:
                return True
        elif self.platform == "pi_pico":
            if self.pin.value() == 1:
                return True
        return False

    def cleanup(self):
        """Limpia la configuración de GPIO."""
        if self.platform == "pi_3":
            self.GPIO.cleanup()

    def __str__(self):
        return (f"Objeto que sirve para detectar movimiento retornando un "
                f"True o 1 cuando lo detecta y contiene las funciones: "
                f"- detecta_moviment() -> Retorna True si detecta movimiento, False en caso contrario. "
                f"- cleanup() -> Limpia la configuración de GPIO.")
