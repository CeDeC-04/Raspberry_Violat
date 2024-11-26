from classe_Buzzer_Passiu_underconstruction_2 import *
import time

BP = Buzzer_Passiu(17, 277)

print(BP)

notes = BP.notes

alarma_incendis = [
    "La7", "Si7", "La7", "Si7", "La7", "Si7", "La7", "Si7",
    "Do8", "Do8", "Do8", "Do8", "Do8", "Do8", "Do8"
]
alarma_gas = [
    "Do8", "Sol7", "Do8", "Sol7", "Mi7", "Fa7", "Mi7", "Fa7",
    "Do8", "Do8", "Re8", "Do8", "Do8"
]
alarma_intrusio = [
    "Do8", "Sol8", "Do8", "Sol8", "Do8", "Sol8", "La7", "La7",
    "Do8", "Do8", "Sol8", "Do8"
]
to_pulsacio = [
    "Sol5", "Do6", "Sol5"
]
to_armat = [
    "Do6", "Mi6", "Sol6"
]
to_desarmat = [
    "Mi5", "Sol5", "Do5"
]
to_notificacio = [
    "Do5", "Fa5", "La5"
]
to_error = [
    "Re5", "Sol5", "Re5"
]
to_confirmacio = [
    "Do6", "Mi6", "Sol6", "Do7"
]

melodies = [alarma_incendis, alarma_gas, alarma_intrusio, to_pulsacio, to_armat, to_desarmat, to_notificacio, to_error, to_confirmacio]
try:
    while True:
        for melodia in melodies:
            for a in "hola":
                for nota in melodia:
                    print(nota, notes[nota])
                    BP.nota(notes[nota])
                    time.sleep(0.125)
            BP.nota(500)   
            time.sleep(2)    
        break





        for nota in notes:
            print(nota, notes[nota])
            BP.nota(notes[nota])
            time.sleep(0.125)
        break
        BP.nota()
        time.sleep(1)
        BP.nota(555)
        time.sleep(1)
        BP.nota(None)
        time.sleep(1)
        print("bip")
    
except KeyboardInterrupt:
    print("aturat")
