import importlib
import time

class Teclat4x4:
    def __init__(self, pins_filas, pins_columnas, platform):
        self.pins_filas = pins_filas
        self.pins_columnas = pins_columnas
        self.platform = platform
        self.teclas_pulsadas = [[False for _ in range(4)] for _ in range(4)]

        if self.platform == "pi_3":
            self.GPIO = importlib.import_module('RPi.GPIO')
            self.GPIO.setmode(self.GPIO.BCM)
            for pin in self.pins_filas:
                self.GPIO.setup(pin, self.GPIO.OUT)
                self.GPIO.output(pin, self.GPIO.HIGH)
            for pin in self.pins_columnas:
                self.GPIO.setup(pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
        elif self.platform == "pi_pico":
            self.GPIO = importlib.import_module('machine')
            self.filas = [self.GPIO.Pin(pin, self.GPIO.OUT) for pin in self.pins_filas]
            self.columnas = [self.GPIO.Pin(pin, self.GPIO.IN, self.GPIO.PULL_DOWN) for pin in self.pins_columnas]

    def scan(self):
        """Escanea todo el teclado y devuelve la tecla presionada una sola vez."""
        tecla = None
        if self.platform == "pi_3":
            for fila in range(len(self.pins_filas)):
                self.GPIO.output(self.pins_filas[fila], self.GPIO.HIGH)
                for columna in range(len(self.pins_columnas)):
                    if self.GPIO.input(self.pins_columnas[columna]) == self.GPIO.HIGH:
                        if not self.teclas_pulsadas[fila][columna]:
                            tecla = [fila, columna]
                            self.teclas_pulsadas[fila][columna] = True
                    else:
                        self.teclas_pulsadas[fila][columna] = False
                self.GPIO.output(self.pins_filas[fila], self.GPIO.LOW)
        
        elif self.platform == "pi_pico":
            for fila in range(len(self.filas)):
                self.filas[fila].high()
                for columna in range(len(self.columnas)):
                    if self.columnas[columna].value() == 1:
                        if not self.teclas_pulsadas[fila][columna]:
                            tecla = [fila, columna]
                            self.teclas_pulsadas[fila][columna] = True
                    else:
                        self.teclas_pulsadas[fila][columna] = False
                self.filas[fila].low()

        return tecla

    def cleanup(self):
        """Limpia la configuración de GPIO."""
        if self.platform == "pi_3":
            self.GPIO.cleanup()