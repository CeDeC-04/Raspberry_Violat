# El programa es comunicarà entre plaques mitjançanmt un diccionari on s'enviarà la part del diccionari que s'hagi modificat entre les 
#plaques. Cada x segons o minuts, s'enviarà el diccionari complert per a comprovar que estigui tot actualitzat (poder una versió següent)
# El programa compararà el diccionari anterior, mitjançant un sort i la creació d'una llista, amb l'actual i compararà si ho ha algun 
#canvi. Si són iguals ignorarà les llibreries i no farà res. Si no és igual, realitzarà l'acció que hagi de fer per a actualitzar
#l'estat dels components.
# També o en substitució, l'alterrnativa seria que agafés una variable buida en la que si ho ha un canvi en algún sensor o en alguna 
#acció cap a un actuador, aquesta variable estarà plena amb el canvi a realitzar i actuarà en consequwencia el sistema, per exemple amb una
#referència del q s'està modificant.

############################       BACKLOG      #################################
#En una primera versió, enviarem només el diccionari dinàmic, la part del diccionari estatic la posarem en un diccionari intern de cada placa.
#Ademés, hi hauran estats dels diccionaris que no s'enviaran a la raspberry i s'haurà de fer en una segona versió

#import machine
#from machine import Pin, I2C
from machine import *
import time
from classe_Buzzer_Passiu_EPS32VROOM import *
#from classe_Buzzer_Passiu import Buzzer_Passiu
from classe_MQ2_esp32 import *
#from classe_MQ2 import MQ2
#import re
from classe_WIFI_ESP32VROOM_2_modChaty import *
#from classe_WIFI_ESP32WROOM import *
#from classe_WIFI_RaspPI3 import *
from classe_pca9685_esp32 import *
from classe_pulsador_esp32 import *
#from classe_pca9685_esp32 import PCA9685
#from classe_pulsador_esp32 import Pulsador
import ujson  # per a MicroPython
#import json # per a Python


# PINs per a sensors i actuadors
    #faltaria passar-ho al chip multiplexor
SENSOR_MAG_ventanas = 17 
    #faltaria passar-ho al chip multiplexor
SENSOR_MAG_puerta = 27 
#####SENSORES_IR_PINes = [22, 23, 24, 25]
BUZZER_PIN = 18
SENSOR_MQ2_PIN = 4


# Creacio objectes
COMs = WIFI()
#Alarma
buzzer = Buzzer_Passiu(BUZZER_PIN)
sensor_gas = MQ2(SENSOR_MQ2_PIN, platform="pi_pico")
    #faltarua passar-ho al chip multiplexor
sensor_mag_serie = machine.Pin(SENSOR_MAG_ventanas, machine.Pin.IN, machine.Pin.PULL_UP) 
    #faltarua passar-ho al chip multiplexor
sensor_mag_indep = machine.Pin(SENSOR_MAG_puerta, machine.Pin.IN, machine.Pin.PULL_UP) 
##########sensores_ir = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in SENSORES_IR_PINes]
#Polsadors i llums
#falta definir polsadors d'alarma, timbre...
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
pulsador = [Pulsador(13, False, "pi_pico"), Pulsador(26, False, "pi_pico"), Pulsador(27, False, "pi_pico"),
            Pulsador(12, False, "pi_pico"), Pulsador(14, False, "pi_pico"), Pulsador(25, False, "pi_pico"),
            Pulsador(33, False, "pi_pico")]
pca = PCA9685(i2c)
pca.freq(50)

# Variables, declaració
missatge_enviar = ''
primerarmat = True
primerDESarmat = False



# diccionaris estàtics
objectes_casa = {
                "Llum_Cuina" : 4,
                "Llum_Passadis" : 2,
                "Llum_Menjador" : 3,
                "Llum_Lavabo" : 5,
                "Llum_Habitació_1" : 1,
                "Llum_Habitació_2" : 6,
                "Llum_Habitació_3" : 7,
                
              ##@  "Led_WIFI_activat" : LED_WIFI_act,
              ##@  "Led_WIFI_conectat" : LED_WIFI_con,
                ##@"Led_WIFI_comunicant" : LED_WIFI_com,
                
                "Pols_Llum_Cuina" : pulsador[0], # Botó teclat 1
                "Pols_Llum_Passadis" : pulsador[1], # Botó teclat 5
                "Pols_Llum_Menjador" : pulsador[2], # Botó teclat 4
                "Pols_Llum_Lavabo" : pulsador[3], # Botó teclat 2
                "Pols_Llum_Habitacio_1" : pulsador[4], # Botó teclat 3
                "Pols_Llum_Habitacio_2" : pulsador[5], # Botó teclat 6
                "Pols_Llum_Habitacio_3" : pulsador[6], # Botó teclat 7
            ##@    "Pols_Servo_Obrir" : Pols_Servo_Obrir, # Botó teclat C
            ##@    "Pols_Servo_Tancar" : Pols_Servo_Tancar, # Botó teclat D
           ##@     "Pols_Timbre" : Pols_Timbre, # Botó teclat 0
           ##@     "Pols_Alarma_Perimetral" : Pols_Alarma_Perimetral, # Botó teclat A
           ##@     "Pols_Alarma_Total" : Pols_Alarma_Total, # Botó teclat B
                
              ##@ "Proximitat_Passadis" : Proximitat_Passadis,
              ##@  "Proximitat_Menjador" : Proximitat_Menjador,
             ##@   "Proximitat_Habitacio_2" : Proximitat_Habitacio_2,
              ##@  "Proximitat_Habitacio_3" : Proximitat_Habitacio_3,
                
              ##@  "Reed_PEntrada" : Reed_PEntrada,
              ##@  "Reed_Menjador" : Reed_Menjador,
             ##@   "Reed_Habitacio_2" : Reed_Habitacio_2,
              ##@  "Reed_Habitacio_3" : Reed_Habitacio_3,
                
                #"Gas_MQ135" : Gas_MQ135, -> 1
                
             ##@   "Servo_PEntrada" : Servo_PEntrada,
                
                #"Alarma_Gas" : Alarma_Gas, -> 1
             ##@   "Alarma_Gas" : sensor_gas,
             #   "Alarma_Intrusió_Perimetral" : alarma_2("Perimetral"), # Ha de contenir els sensors reed
              #  "Alarma_Intrusió_Total" : alarma_2("Total") # Ha de contenir els sensors de proximitat i els reed
                "Alarma_Intrusió_Perimetral" : '',
                "Alarma_Intrusió_Total" : ''
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
                
                "Servo_PEntrada" : False, # False està tancada 0, #0-90 graus obertura
                
                "Alarma_Gas" : False, #Pot ser True or False (detectat/no detectat)
                "Alarma_Intrusio_Perimetral" : "FF", # Armat/activat {False, False} #Pot ser True or False tant l'armat (armat/desarmat) com detecció (detectat/no detectat)
                "Alarma_Intrusio_Total" : "FF" # Armat/activat {False, False} #Pot ser True or False tant l'armat (armat/desarmat) com detecció (detectat/no detectat)
                }


def to_diccionari(text): # Per a MicroPython
    try:
        # Converteix el text JSON en un diccionari Python
        return ujson.loads(text)
    except ValueError as e:
        # Captura errors en cas de text no vàlid
        print(f"Error en convertir el text a diccionari: {e}")
        return '{}'


#### Alarma
#### Alarma
#### Alarma
#### Alarma

# Función para verificar sensores ALARMA INTRUSSIÓ
def verificar_sensores(modo): # CeDeC: no entenc que fa
    if modo == "Perimetral":
        return sensor_mag_serie.value() == 0 or sensor_mag_indep.value() == 0
    elif modo == "Total":
        if verificar_sensores("Perimetral"):
            return True
        return any(sensor.value() == 0 for sensor in sensores_ir)
    return False

# Función para monitorear el sensor de gas
def verificar_gas2():
    if sensor_gas.detecta_particules():
        estat_objectes_casa["Alarma_Gas"] = True
        buzzer.melodia("alarma_gas")
    else:
        estat_objectes_casa["Alarma_Gas"] = False
        buzzer.desactiva()

def verificar_gas():
    if sensor_gas.detecta_particules():
        print("¡Gas detectado!")
        estat_objectes_casa["Alarma_Gas"] = True
        buzzer.melodia("alarma_gas")

#primerarmat = True
#primerDESarmat = False

# Función principal de la alarma
def alarma_2(modo):
    global primerarmat, primerDESarmat
    verificar_gas2()
    if estat_objectes_casa[f"Alarma_Intrusio_{modo}"][0] == "T":
        if primerarmat:
            armar_alarma(modo)
            primerarmat,primerDESarmat = False, True
        if estat_objectes_casa[f"Alarma_Intrusio_{modo}"][1] == "T":
            if verificar_sensores(modo):
                buzzer.melodia("alarma_intrusio")
#            else:
#                buzzer.desactiva()
    elif estat_objectes_casa[f"Alarma_Intrusio_{modo}"][0] == "F":
        if primerDESarmat:
            desarmar_alarma2(modo)
            primerarmat,primerDESarmat = True, False

def alarma(modo):
    print(f"Alarma activada en modo: {modo.upper()}")
    buzzer.melodia("to_armat")
    estat_objectes_casa[f"Alarma_Intrusio_{modo.capitalize()}"] = "TT"  # Armat y Activo
    try:
        while estat_objectes_casa[f"Alarma_Intrusio_{modo.capitalize()}"] == "TT":
            verificar_gas()
            if verificar_sensores(modo):
                print("¡Alarma activada!")
                buzzer.melodia("alarma_intrusio")
                time.sleep(2)
            time.sleep(0.1)
    except KeyboardInterrupt:
        desarmar_alarma(modo)

def armar_alarma(modo):
    estat_objectes_casa[f"Alarma_Intrusio_{modo.capitalize()}"][0] = "T"  # Armat
    buzzer.melodia("to_armat")

def desarmar_alarma2(modo):
    estat_objectes_casa[f"Alarma_Intrusio_{modo.capitalize()}"][0] = "F"  # Desarmat
    buzzer.desactiva()
    time.sleep(0.5)
    buzzer.melodia("to_desarmat")
    
def desarmar_alarma(modo):
    print(f"Alarma desactivada: {modo.upper()}")
    estat_objectes_casa[f"Alarma_Intrusio_{modo.capitalize()}"] = "FF"  # Desarmat y No Activo
    buzzer.melodia("to_desarmat")


### Polsadors
### Polsadors
### Polsadors
### Polsadors

def detectar_pulsadors():
    keys_pols = ["Pols_Llum_Cuina", "Pols_Llum_Passadis", "Pols_Llum_Menjador", "Pols_Llum_Lavabo",
            "Pols_Llum_Habitació_1", "Pols_Llum_Habitació_2", "Pols_Llum_Habitació_3"]
    keys_llum = ["Llum_Cuina", "Llum_Passadis", "Llum_Menjador", "Llum_Lavabo",
            "Llum_Habitació_1", "Llum_Habitació_2", "Llum_Habitació_3"]

    for key in range(len(keys_pols)):
        accion = objectes_casa[keys_pols[key]].gestionar_pulsacions(1)
        
        if accion[0] == True:
            pca.alterna(objectes_casa[keys_llum[key]])
            pca.bajando = True
        elif accion[1] == True:
            pca.bajar_subir(objectes_casa[keys_llum[key]])
        
        if accion[0] or accion[1]:
            estat_objectes_casa[keys_llum[key]] == True
        else:
            estat_objectes_casa[keys_llum[key]] == False



estat_objectes_casa["Alarma_Intrusió_Perimetral"] = alarma_2("Perimetral") # Ha de contenir els sensors reed
estat_objectes_casa["Alarma_Intrusió_Total"] = alarma_2("Total") # Ha de contenir els sensors de proximitat i els reed

while True:
    
    try:
        # Realitza comunicacio
        missatge_rebut = COMs.WIFI_comunicacio('{}')
        missatge_enviar = '{}' #els {} s'han de possar si hi ha algun canvi a enviar
        #en la primera versió, es suposa que a cada tecla s'envia el missatge. pero es possible que en altres versions s'enviin ´es canvis en un enviament i en fils
        
        # Actualitza diccionari si es rebut algun canvi
        if missatge_rebut != '':
            diccionari_rebut = to_diccionari(missatge_rebut)
            claus_novetat = diccionari_rebut.keys()

            for key in claus_novetat:
                estat_objectes_casa[key] = diccionari_rebut[key]
                if "Llum" in key:
                    pca.alterna(key)
                    '''



 ########
                fer que ejecute los cambios


#########        
        # Diccionari anterior
        diccionari_estats_anterior = sorted(estat_objectes_casa.items()) # Ordena segons les claus    

        creació de la variable del diccionari a enviar en mode text

#########
        apartat 'BBBB
        capta els valors dels sensors #fer les coses seguint els sensors
        el diccionari s'actualitza a cada sensor pel que passa
        així mateix la variable string del diccionari a enviar a la raspberry també s'actualitza
        # Verificación de estado de la alarma

        
#########        
        if diccionari ara != a abans, entra i canvia coses. Si és el mateix significa que no ha passat res i nno cal q faci res
        llegeix el diccionari i actualitza l'estat dels actuadors (llums, buzzer, servo...) en funció del nou valor del diccionari que ha aportat el sensor corresponent
        #el diccionari s'haur``a actualitzat despres de pasar per codi
                    '''
        
        
        if estat_objectes_casa["Alarma_Intrusio_Total"][0] == "T": #l'armat Total te prioritat        
            alarma_2("Total")
        elif estat_objectes_casa["Alarma_Intrusio_Perimetral"][0] == "T": #si no esta total comprova si esta perimetral
            alarma_2("Perimetral")
        else:
            alarma_2("Total") #podria ser alarma_2("Perimetral"), tant ne fa pq estan desarmades les dues

        detectar_pulsadors()
        '''
##        
fer una funció per objecte o si pot ser per grup d'objectes que es cridara en l'apartat 'BBBB
  ##      
        '''  
  
  
    except Exception as e:
        print("Error:", e)
    except KeyboardInterrupt:
        print("Apagando sistema...")
        break
        # Canvi en el diccionari
        
'''       # Crea el missatge a enviar, si no hi ha canvis, envia text buit
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
 '''
 
        

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
