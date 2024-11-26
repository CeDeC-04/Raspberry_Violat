import RPi.GPIO as GPIO
import time

class SensorPIR:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)  # Mode de numeració de pins com BCM
        GPIO.setup(self.pin, GPIO.IN)  # Configura el pin del PIR com a entrada

    def detecta_moviment(self):
        """Retorna True si detecta moviment, False en cas contrari."""
        if GPIO.input(self.pin) == GPIO.HIGH:
            return True
        else:
            return False

    def cleanup(self):
        """Neteja la configuració de GPIO."""
        GPIO.cleanup()

    def __str__(self):
        return (f"Objecte que serveix per a detectar moviment retornant un"
                f"True o 1 quan el detecta i conté les funcions"
                f"- detecta_moviment()  -> Retorna True si detecta moviment, False en cas contrari."
                f"- cleanup() -> Neteja la configuració de GPIO.")
