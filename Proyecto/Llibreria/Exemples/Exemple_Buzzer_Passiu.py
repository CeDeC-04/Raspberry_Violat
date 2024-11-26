from classe_Buzzer_Passiu import *
import time

BP = Buzzer_Passiu(17, 277)

try:
    while True:

        BP.nota("Re5")
        time.sleep(0.125)
        BP.desactiva()

        for nota in BP.notes:
            BP.nota(nota)
            time.sleep(0.125)
            BP.desactiva()
            print(nota)

        iok,iko = 0,0
         
        for melodia in BP.melodies:
            print(melodia, end = (' '), flush = True)
            if BP.melodia(melodia, 0.125):
                print("-> tot ha anat bé")
                BP.desactiva()
                time.sleep(1)
                iok += 1
            else:
                print("-> hi ha hagut un ERROR")
                iko += 1
        if iok == 0:
            print("No s'ha reproduït cap melodia per ERRORs")
        elif iko == 0:
            print("S'ha reproduït totes les melodies amb ÉXIT")
        else:
            print("S'han reproduït {iok} melodies amb ÉXIT"
                  "No s'han reproduït {iko} melodies per ERRORs")
       
except KeyboardInterrupt:
    print("aturat")
