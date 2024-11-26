import RPi.GPIO as GPIO
import time

class Pulsador:
    def __init__(self, pin, state):
        """Constructor del Objeto"""
        self.pin = pin
        GPIO.setmode(GPIO.BCM)  
        if state:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.state = state
        self.temps_anterior = time.time()
        self.actiu = False

    def detecta_pulsacio(self):
        """Retorna True si detecta pulsacio, False en cas contrari."""
        if GPIO.input(self.pin) == self.state:
            return True
        else:
            return False
        
    def unica_pulsacio(self):
        """Retorna una unica pulsacio"""
        if self.detecta_pulsacio():
            if self.actiu == False:
                self.actiu = True
                return True
        else:
            self.actiu = False   
        return False
        
    def mesura_pulsacio(self):
        """Mesura el temps de pulsacio."""
        start_time = time.time()
        while self.detecta_pulsacio() == GPIO.HIGH:
            time.sleep(0.01)
            
        temps = time.time() - start_time
        return temps
  
    def interval_pulsacio(self, temps):
        current_time = time.time()
        if current_time - self.temps_anterior >= temps:
            self.temps_anterior = current_time
            return True
        return False

    def temps_pulsat(self, temps):
        current_time = time.time()
        if self.detecta_pulsacio():
            if self.interval_pulsacio(temps):
                self.temps_anterior = current_time
                return True
        else:
            self.temps_anterior = current_time
        return False

 
    def cleanup(self):
        """Neteja la configuració de GPIO."""
        GPIO.cleanup()