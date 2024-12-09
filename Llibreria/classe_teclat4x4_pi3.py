import RPi.GPIO as GPIO
import time


class Teclat4x4:
    
    def __init__(self, pins_filas, pins_columnas, teclas = [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]):
        self.pins_filas = pins_filas
        self.pins_columnas = pins_columnas
        self.teclas_pulsadas = [[False for _ in range(4)] for _ in range(4)]
        self.teclas = teclas

        GPIO.setmode(GPIO.BCM)
        for pin in self.pins_filas:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        for pin in self.pins_columnas:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def scan(self):
        """Escanea todo el teclado y devuelve la matriu de la tecla una sola vez."""
        tecla = None
        for fila in range(len(self.pins_filas)):
            GPIO.output(self.pins_filas[fila], GPIO.HIGH)
            for columna in range(len(self.pins_columnas)):
                if GPIO.input(self.pins_columnas[columna]) == GPIO.HIGH:
                    if not self.teclas_pulsadas[fila][columna]:
                        tecla = [fila, columna]
                        self.teclas_pulsadas[fila][columna] = True
                else:
                    self.teclas_pulsadas[fila][columna] = False
            GPIO.output(self.pins_filas[fila], GPIO.LOW)

        return tecla


    def tecla(self):
        """Escanea todo el teclado y devuelve la tecla presionada una sola vez."""
        tecla = self.scan()
        if tecla == None:
            return tecla
        else:
            return self.teclas[tecla[0]][tecla[1]]


    def cleanup(self):
        """Limpia la configuración de GPIO."""
        self.GPIO.cleanup()
