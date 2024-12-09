from machine import Pin
import time

class Pulsador:
    def __init__(self, pin, state, platform = ''):
        """Constructor del Objeto"""
        self.pin = pin
        self.platform = platform
        
        if state:
            self.pin = Pin(self.pin, Pin.IN, Pin.PULL_UP)
        else:
            self.pin = Pin(self.pin, Pin.IN, Pin.PULL_DOWN)
        
        self.state = state
        self.temps_anterior = time.time()
        self.actiu = False
        self.accion_corta_realizada = False 
        self.pulsacion_larga_iniciada = False

    def detecta_pulsacio(self):
        """Retorna True si detecta pulsacio, False en caso contrario."""
        if self.pin.value() == self.state:
                return True
        return False
        
    def unica_pulsacio(self):
        """Retorna una unica pulsacion."""
        if self.detecta_pulsacio():
            if not self.actiu:
                self.actiu = True
                return True
        else:
            self.actiu = False   
        return False

    def interval_pulsacio(self, temps):
        """Gestiona el tiempo entre pulsaciones."""
        current_time = time.time()
        if current_time - self.temps_anterior >= temps:
            self.temps_anterior = current_time
            return True
        return False

    def temps_pulsat(self, temps):
        """Retorna True si el botón se mantiene presionado por más de un tiempo determinado."""
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
