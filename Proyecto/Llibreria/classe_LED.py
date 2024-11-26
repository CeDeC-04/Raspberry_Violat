import RPi.GPIO as GPIO
import time
#from machine import Pin, PWM

class LED:
    intensitats = [5, 15, 30, 50, 75, 100]
    def __init__(self, pin, intensitat):
        """Constructor del Objeto"""
        self.pin = pin
        self.intensitat = intensitat
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.pin, GPIO.OUT) 
        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(self.intensitats[intensitat])
        self.state = False
        self.temps_anterior = time.time()
    
    def encen(self):
        """Encén el LED."""
        self.cambia_intensitat(self.intensitats[self.intensitat])
        self.state = True        
    
    def apaga(self):
        """Apaga el LED."""
        self.cambia_intensitat(0)
        self.state = False
    
    '''
    def intensitat(self, intensitat):
        """Canvia l'intensitat del LED."""
        self.pwm = PWM(Pin(self.pin))
        self.pwm.freq(1000)

        self.pwm.duty_u16(intensitat)
    '''
    def cambia_intensitat(self, intensitat):
        """Canvia l'intensitat del LED, el rang es de 0 a 100."""
        self.pwm.ChangeDutyCycle(intensitat)

    def aumenta_intensitat(self):
        """Aumenta l'intensitat del LED."""
        if self.intensitat < len(self.intensitats) - 1:
            self.intensitat += 1
            self.cambia_intensitat(self.intensitats[self.intensitat])
           
    def treu_intensitat(self):
        """Disminueix l'intensitat del LED."""
        if self.intensitat > 0:
            self.intensitat -= 1
            self.cambia_intensitat(self.intensitats[self.intensitat])  

    def pampalluga(self, temps):
        """Canvia l'estat del LED cada X segoons, sen X la cuantitat introduida."""
        current_time = time.time()
        
        if current_time - self.temps_anterior >= temps:
            self.alterna()
            self.temps_anterior = current_time
       
    def alterna(self):
        """Canvia l'estat del LED."""
        if self.state:
            self.apaga()
        else:
            self.encen()
    
    def cleanup(self):
        """Neteja la configuració de GPIO."""
        GPIO.cleanup()