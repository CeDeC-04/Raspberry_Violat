import RPi.GPIO as GPIO
import time

class Pulsador:
    def __init__(self, pin, state, platform):
        """Constructor del Objeto"""
        self.pin = pin
        self.platform = platform
        
        GPIO.setmode(self.GPIO.BCM)
        if state:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.state = state
        self.temps_anterior = time.time()
        self.actiu = False
        self.accion_corta_realizada = False 
        self.pulsacion_larga_iniciada = False

    def detecta_pulsacio(self):
        """Retorna True si detecta pulsacio, False en cas contrari."""
        if GPIO.input(self.pin) == self.state:
            return True
        return False
        
    def unica_pulsacio(self):
        """Retorna una unica pulsacio"""
        if self.detecta_pulsacio():
            if not self.actiu:
                self.actiu = True
                return True
        else:
            self.actiu = False   
        return False
        
    def mesura_pulsacio(self):
        """Mesura el temps de pulsacio."""
        start_time = time.time()
        while self.detecta_pulsacio():
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

    def gestionar_pulsacions(self, temps=1):
        """Gestiona pulsación corta y larga."""
        if self.detecta_pulsacio():
            tiempo_presionado = time.time() - self.temps_anterior
            if tiempo_presionado < temps:
                # Pulsación corta
                if not self.accion_corta_realizada:
                    self.accion_corta_realizada = True
                    self.pulsacion_larga_iniciada = False
                    return [self.accion_corta_realizada, self.pulsacion_larga_iniciada]
            elif tiempo_presionado >= temps:
                # Pulsación larga
                if not self.pulsacion_larga_iniciada:
                    self.accion_corta_realizada = False
                    self.pulsacion_larga_iniciada = True
                    #return "Acción para pulsación larga iniciada"
                else:
                    return [self.accion_corta_realizada, self.pulsacion_larga_iniciada]
        else:
            self.accion_corta_realizada = False
            self.pulsacion_larga_iniciada = False
            self.temps_anterior = time.time()
        return [False, False]

    def cleanup(self):
        """Limpia la configuración de GPIO."""
        GPIO.cleanup()