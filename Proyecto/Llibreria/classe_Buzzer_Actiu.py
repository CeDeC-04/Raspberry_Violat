import RPi.GPIO as GPIO
import time

class Buzzer_Actiu:
    def __init__(self, buzzer_pin):
        self.pin = buzzer_pin
        GPIO.setmode(GPIO.BCM)  # Mode de numeració de pins
        GPIO.setup(self.pin, GPIO.OUT)  # Configura el pin del buzzer com a sortida

    def encen(self):
        """Activa el buzzer (so)."""
        GPIO.output(self.pin, GPIO.HIGH)
        

    def apaga(self):
        """Desactiva el buzzer (sense so)."""
        GPIO.output(self.pin, GPIO.LOW)
       
    def sonar_durant(self, segons):
        """Fa sonar el buzzer durant un cert temps (en segons)."""
        self.encendre()
        time.sleep(segons)
        self.apagar()

    def cleanup(self):
        """Neteja la configuració de GPIO."""
        GPIO.cleanup()
