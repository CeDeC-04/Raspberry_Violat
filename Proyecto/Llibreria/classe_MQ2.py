import RPi.GPIO as GPIO
import time

class MQ2:
    def __init__(self, pin):
        """Constructor del Objeto"""
        self.pin = pin
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.pin, GPIO.IN)
    
    def detecta_particules(self):
        """Retorna True si detecta particules, False en cas contrari."""
        if GPIO.input(self.pin) == GPIO.LOW:
            return True
        return False
 
    def cleanup(self):
        """Neteja la configuració de GPIO."""
        GPIO.cleanup()