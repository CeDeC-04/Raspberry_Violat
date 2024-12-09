from classe_teclat4x4 import *

teclas = [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]

teclado = Teclat4x4([21, 20, 16, 12], [25, 24, 23, 18], "pi_pico")

try:
    while True:
        tecla = teclado.scan()
        if tecla is not None:
            print("Tecla presionada: ", teclas[tecla[0]][tecla[1]])
            print("Lletra: ", teclado.tecla())
            time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
