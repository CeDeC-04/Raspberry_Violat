# El programa es comunicarà entre plaques mitjançanmt un diccionari on s'enviarà la part del diccionari que s'hagi modificat entre les 
#plaques. Cada x segons o minuts, s'enviarà el diccionari complert per a comprovar que estigui tot actualitzat (poder una versió següent)
# El programa compararà el diccionari anterior, mitjançant un sort i la creació d'una llista, amb l'actual i compararà si ho ha algun 
#canvi. Si són iguals ignorarà les llibreries i no farà res. Si no és igual, realitzarà l'acció que hagi de fer per a actualitzar
#l'estat dels components.
# També o en substitució, l'alterrnativa seria que agafés una variable buida en la que si ho ha un canvi en algún sensor o en alguna 
#acció cap a un actuador, aquesta variable estarà plena amb el canvi a realitzar i actuarà en consequwencia el sistema, per exemple amb una
#referència del q s'està modificant.

#estat_casa = { llum_menjador : {llums,5}, llum_cuina : {llums,0}, sensor_gas : {gas,0}, estat_alarma : {alarma,{"armada","desactivada"}}}
#estat_casa = { llum : {menjador : 5}, llum : {cuina : 0}, gas : {mq135 : 0}, {alarma : {alarma : {"armada","desactivada"}}}
#keys_estat_casa = { llum : "llum", gas : "gas", alarma : "alarma"}
#estat_casa = { llum_menjador : 5, llum_cuina : 0, gas_cuina : 0, alarma_general : {"armada","desactivada"}}

#objecte_casa = { llum_menjador : pcaLM, llum_cuina : pcaLC, gas_cuina : mq1351, alarma_general : alarmaG}
#estat_casa = { llum_menjador : "5T" '''(aixó seria valor 5% i True, és a dir encés. Si fos F, seria apagat (False))''', llum_cuina : 0, gas_cuina : 0, alarma_general : {"armada","desactivada"}}

#estat_casa = { "llum_menjador" : {"estat" : 5, "objecte" : llum_M}, "alarmaGeneral": {"estat": "activada", "armada" : True, "objecte": "alarmaGeneral"},

#En una primera versió, enviarem només el diccionari dinàmic, la part del diccionari estatic la posarem en un diccionari intern de cada placa.

import re
from classe_WIFI_RaspPI3.py import *
import ujson  # per a MicroPython
#import json # per a Python

missatge_enviar = '{}'

# Creacio objectes
COMs = WIFI()


while True:
    
    try:
        # Realitza comunicacio
        missatge_rebut = COMs.WIFI_Comunicacio(missatge_enviar)
        missatge_enviar = '{}' #en la primera versió, es suposa que a cada tecla s'envia el missatge. pero es possible que en altres versions s'enviin ´es canvis en un enviament i en fils

        # Actualitza diccionari si es rebut algun canvi
        if missatge_rebut != '':
            diccionari_rebut = to_diccionari(missatge_rebut)
            claus_novetat = diccionari_rebut.keys()
            
            for key in claus_novetat:
                estat_objectes_casa[key] = diccionari_rebut[key]
        
        # Crea el missatge a enviar, si no hi ha canvis, envia text buit
        clau = Teclat.tecla()
        if clau != None:
            if "Llum" in clau:
                fi = ''
                if estat_objectes_casa[clau][-1] == "F":
                    fi = "T"
                else:
                    fi = "F"
                estat_objectes_casa[clau] = estat_objectes_casa[clau][:-1]+fi
                missatge_enviar = missatge_enviar[:-1]+clau+f': {estat_objectes_casa[clau]}'+f'{missatge_enviar[len(missatge_enviar)-1]}'#estat_objectes_casa[clau]})' #en la primera versió, es suposa que a cada tecla s'envia el missatge. pero es possible que en altres versions s'enviin ´es canvis en un enviament i en fils
            elif "Intrusio" in clau: # Aquí només armarà o desarmarà l'alarma
                ini = ''
                if estat_objectes_casa[clau][-1] == "F":
                    ini = "T"
                else:
                    ini = "F"
                estat_objectes_casa[clau] = ini+estat_objectes_casa[clau][-1]
                missatge_enviar = missatge_enviar[:-1]+clau+f': {estat_objectes_casa[clau]}'+f'{missatge_enviar[len(missatge_enviar)-1]}'
                        #estat_objectes_casa[clau]})'#en la primera versió, es suposa que a cada tecla s'envia el missatge. pero es possible que en altres versions s'enviin ´es canvis en un enviament i en fils
            else:
                estat_objectes_casa[clau] = not estat_objectes_casa[clau]
                missatge_enviar = missatge_enviar[:-1]+clau+f': {estat_objectes_casa[clau]}'+f'{missatge_enviar[len(missatge_enviar)-1]}'
    except KeyboardInterrupt:
        print("Aturada manual per l'usuari")
 
def to_diccionari(text): # Per a MicroPython
    try:
        # Converteix el text JSON en un diccionari Python
        return ujson.loads(text)
    except ValueError as e:
        # Captura errors en cas de text no vàlid
        print(f"Error en convertir el text a diccionari: {e}")
        return {}

''' 
def to_diccionari(text): # Per a Python
    # Regex per capturar la clau i el valor
    pattern = r'"(\w+)"\s*:\s*({.*?}|\d+|"[^"]*")'
    matches = re.findall(pattern, text)
    
    diccionari = {}
    for key, value in matches:
        # Comprovem si el valor és un conjunt (set)
        if value.startswith("{"):  
            # Eliminem les cometes i convertim els valors dins de les claus en tipus corresponents
            value = value.strip("{}").split(",")
            diccionari[key] = {val.strip() for val in value}
        elif value.isdigit():  # Si el valor és un número
            diccionari[key] = int(value)
        else:  # Si el valor és una cadena
            diccionari[key] = value.strip('"')
    
    return diccionari
'''           

# configuracio sortida tecles del teclat
#equivalencia a -> [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]
Tecles = [["Pols_Llum_Cuina", "Pols_Llum_Lavabo", "Pols_Llum_Habitacio_1", "Pols_Alarma_Perimetral"], # -> [["1", "2", "3", "A"],
          ["Pols_Llum_Menjador", "Pols_Llum_Passadis", "Pols_Llum_Habitacio_2", "Pols_Alarma_Total"], # -> ["4", "5", "6", "B"],
          ["Pols_Llum_Habitacio_3", "8", "9", "Pols_Servo_Obrir"], # -> ["7", "8", "9", "C"],
          ["*", "Pols_Timbre", "#", "Pols_Servo_Tancar"]] # -> ["*", "0", "#", "D"]]

# diccionaris estàtics
objectes_casa = {
                "Llum_Cuina" : Llum_Cuina_PCA,
                "Llum_Passadis" : Llum_Passadis_PCA,
                "Llum_Menjador" : Llum_Menjador_PCA,
                "Llum_Lavabo" : Llum_Lavabo_PCA,
                "Llum_Habitació_1" : Llum_Habitació_1,
                "Llum_Habitació_2" : Llum_Habitació_2,
                "Llum_Habitació_3" : Llum_Habitació_3,
                
                "Led_WIFI_activat" : LED_WIFI_act
                "Led_WIFI_conectat" : LED_WIFI_con
                "Led_WIFI_comunicant" : LED_WIFI_com
                
                "Pols_Llum_Cuina" : Pols_Llum_Cuina_PCA, # Botó teclat 1
                "Pols_Llum_Passadis" : Pols_Llum_Passadis_PCA, # Botó teclat 5
                "Pols_Llum_Menjador" : Pols_Llum_Menjador_PCA, # Botó teclat 4
                "Pols_Llum_Lavabo" : Pols_Llum_Lavabo_PCA, # Botó teclat 2
                "Pols_Llum_Habitacio_1" : Pols_Llum_Habitacio_1, # Botó teclat 3
                "Pols_Llum_Habitacio_2" : Pols_Llum_Habitacio_2, # Botó teclat 6
                "Pols_Llum_Habitacio_3" : Pols_Llum_Habitacio_3, # Botó teclat 7
                "Pols_Servo_Obrir" : Pols_Servo_Obrir, # Botó teclat C
                "Pols_Servo_Tancar" : Pols_Servo_Tancar, # Botó teclat D
                "Pols_Timbre" : Pols_Timbre, # Botó teclat 0
                "Pols_Alarma_Perimetral" : Pols_Alarma_Perimetral, # Botó teclat A
                "Pols_Alarma_Total" : Pols_Alarma_Total, # Botó teclat B
                
                "Proximitat_Passadis" : Proximitat_Passadis,
                "Proximitat_Menjador" : Proximitat_Menjador,
                "Proximitat_Habitacio_2" : Proximitat_Habitacio_2,
                "Proximitat_Habitacio_3" : Proximitat_Habitacio_3,
                
                "Reed_PEntrada" : Reed_PEntrada,
                "Reed_Menjador" : Reed_Menjador,
                "Reed_Habitacio_2" : Reed_Habitacio_2,
                "Reed_Habitacio_3" : Reed_Habitacio_3,
                
                #"Gas_MQ135" : Gas_MQ135, -> 1
                
                "Servo_PEntrada" : Servo_PEntrada,
                
                #"Alarma_Gas" : Alarma_Gas, -> 1
                "Alarma_Gas" : Gas_MQ135,
                "Alarma_Intrusió_Perimetral" : Alarma_Intrusió_Perimetral, # Ha de contenir els sensors reed
                "Alarma_Intrusió_Total" : Alarma_Intrusió_Total # Ha de contenir els sensors de proximitat i els reed
                }

# diccionaris dinàmics
estat_objectes_casa = {
                "Llum_Cuina" : "100F", #Pot ser del mínim 5% (5) per exemple fins al 100% (100), apagat (F) o encés (T) ->exemple 5T 100F
                "Llum_Passadis" : "100F",
                "Llum_Menjador" : "100F",
                "Llum_Lavabo" : "100F",
                "Llum_Habitacio_1" : "100F",
                "Llum_Habitacio_2" : "100F",
                "Llum_Habitacio_3" : "100F",
                
                "Led_WIFI_activat" : False,
                "Led_WIFI_conectat" : False, 
                "Led_WIFI_comunicant" : False, # Blinking
                
                "Pols_Llum_Cuina" : False, #Poden ser True or False (polsat/no polsat)
                "Pols_Llum_Passadis" : False,
                "Pols_Llum_Menjador" : False,
                "Pols_Llum_Lavabo" : False,
                "Pols_Llum_Habitacio_1" : False,
                "Pols_Llum_Habitacio_2" : False,
                "Pols_Llum_Habitacio_3" : False,
                "Pols_Servo_Obrir" : False,
                "Pols_Servo_Tancar" : False,
                "Pols_Timbre" : False, 
                "Pols_Alarma_Perimetral" : False,
                "Pols_Alarma_Total" : False,
                
                "Proximitat_Passadis" : False, #Poden ser True or False (detectat/no detectat)
                "Proximitat_Menjador" : False,
                "Proximitat_Habitacio_2" : False,
                "Proximitat_Habitacio_3" : False,
                
                "Reed_PEntrada" : False, #Poden ser True or False (tancat/obert)
                "Reed_Menjador" : False,
                "Reed_Habitacio_2" : False,
                "Reed_Habitacio_3" : False,
                
                #"Gas_MQ135" : Gas_MQ135, -> 1
                
                "Servo_PEntrada" : False, # False està tancada 0, #0-90 graus obertura
                
                #"Alarma_Gas" : Alarma_Gas, -> 1
                "Alarma_Gas" : False, #Pot ser True or False (detectat/no detectat)
                "Alarma_Intrusio_Perimetral" : "FF", # Armat/activat {False, False} #Pot ser True or False tant l'armat (armat/desarmat) com detecció (detectat/no detectat)
                "Alarma_Intrusio_Total" : "FF" # Armat/activat {False, False} #Pot ser True or False tant l'armat (armat/desarmat) com detecció (detectat/no detectat)
                }
