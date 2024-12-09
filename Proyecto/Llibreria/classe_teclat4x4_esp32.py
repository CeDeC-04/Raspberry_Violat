from machine import Pin
import time


class Teclat4x4:
    
    def __init__(self, pins_filas, pins_columnas, platform, teclas = [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]):
        self.pins_filas = pins_filas
        self.pins_columnas = pins_columnas
        self.platform = platform
        self.teclas_pulsadas = [[False for _ in range(4)] for _ in range(4)]
        self.teclas = teclas

        if self.platform == "pi_pico":
            self.filas = [Pin(pin, Pin.OUT) for pin in self.pins_filas]
            self.columnas = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in self.pins_columnas]


    def scan(self):
        """Escanea todo el teclado y devuelve la matriu de la tecla una sola vez."""
        tecla = None

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


    def tecla(self):
        """Escanea todo el teclado y devuelve la tecla presionada una sola vez."""
        tecla = self.scan()

        return self.teclas[tecla[0]][tecla[1]]
