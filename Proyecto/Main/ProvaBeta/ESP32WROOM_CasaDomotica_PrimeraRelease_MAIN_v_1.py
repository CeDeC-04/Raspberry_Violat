'''
Arxiu anterior: 
    1-main_BetaPasaPas_20241208.py -> wifi funcions funcional
      main_WIFI_BetaPasaPas_20241208.py -> ni puta idea, crec q es el mateix
    1bis- canvi de nom de main_CasaDomotica_PrimeraRelease_v_0.py a main_ESP32WROOM_CasaDomotica_PrimeraRelease_v_1.py
    2- main_ESP32WROOM_CasaDomotica_PrimeraRelease_v_1.py -> res funciona, es refa de nou la classe (classe_WIFI_ESP32WROOM.py) i es procedeix a seguir en aquesta versió
    3- ESP32WROOM_CasaDomotica_PrimeraRelease_MAIN_v_0.py -> versió funcional de creació objectes, assignació de valors, etc amb MAIN de prova
    
'''
'''
Accions en aquest ongoing:
    seguint feina de l'arxiu 3- on es segueix amb el merge del "main" de ESP32VROOM_CasaDomotica_v_3_merged_prova_beta.py 
'''
from machine import *
import ujson  # per a MicroPython
#import json # per a Python

from classe_WIFI_ESP32WROOM import *
from classe_Buzzer_Passiu_EPS32VROOM import *
from classe_MQ2_esp32 import *
from classe_pca9685_esp32 import *
from classe_pulsador_esp32 import *



                ###### Assignació PINs ######
PIN_Reed_finestra = 17 #Els reed estan en serie, en aquesta versió no es sabrà quin ha saltat
PIN_Reed_portaEnt = 27 
BUZZER_PIN = 18
SENSOR_MQ2_PIN = 4


                ###### Assignació variables ######
missatge_enviar = '{}'
primerarmat = True
primerDESarmat = False


                ###### Creació objectes ######
# WIFI
COMs = WIFI()

# Alarma
Buzzer = Buzzer_Passiu(BUZZER_PIN)
Sensor_gas = MQ2(SENSOR_MQ2_PIN, platform = "tant ne carda en aquesta versió ESP_32")
ReedFinestres = machine.Pin(PIN_Reed_finestra, machine.Pin.IN, machine.Pin.PULL_UP) #"_Alarma_en_serie"
ReedPortaEnt = machine.Pin(PIN_Reed_portaEnt, machine.Pin.IN, machine.Pin.PULL_UP) 

# Polsadors i llums
    #falta definir polsadors d'alarma, timbre...
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
polsador = [Pulsador(13, False), Pulsador(26, False), Pulsador(27, False),
            Pulsador(12, False), Pulsador(14, False), Pulsador(25, False),
            Pulsador(33, False)]
pca = PCA9685(i2c)
pca.freq(50)
                
                
                ###### Creació de funcions ######
def to_diccionari(text): # Per a MicroPython
    try:
        # Converteix el text JSON en un diccionari Python
        return ujson.loads(text)
    except ValueError as e:
        # Captura errors en cas de text no vàlid
        print(f"Error en convertir el text a diccionari: {e}")
        return '{}'


#### Alarma #### Alarma #### Alarma


# Funció per a verificar sensors d'ALARMA INTRUSSIÓ
def verificar_sensores(mode): # CeDeC: no entenc que fa
    if mode == "Perimetral":
        return sensor_mag_serie.value() == 0 or sensor_mag_indep.value() == 0
    elif mode == "Total":
        if verificar_sensores("Perimetral"):
            return True
        return any(sensor.value() == 0 for sensor in sensores_ir)
    return False

# Funció per a monitoratge del sensor de gas
def verificar_gas2():
    if Sensor_gas.detecta_particules():
        estat_objectes_casa["Alarma_Gas"] = True
        Buzzer.melodia("alarma_gas")
    else:
        estat_objectes_casa["Alarma_Gas"] = False
        Buzzer.desactiva()
        
# Funció principal de la alarma
def alarma_2(mode):
    global primerarmat, primerDESarmat
    verificar_gas2()
    if estat_objectes_casa[f"Alarma_Intrusio_{mode}"][0] == "T":
        if primerarmat:
            armar_alarma(mode)
            primerarmat,primerDESarmat = False, True
        if estat_objectes_casa[f"Alarma_Intrusio_{mode}"][1] == "T":
            if verificar_sensores(mode):
                Buzzer.melodia("alarma_intrusio")
    elif estat_objectes_casa[f"Alarma_Intrusio_{mode}"][0] == "F":
        if primerDESarmat:
            desarmar_alarma2(mode)
            primerarmat,primerDESarmat = True, False

def armar_alarma(mode):
    estat_objectes_casa[f"Alarma_Intrusio_{mode}"][0] = "T"  # Armat
    Buzzer.melodia("to_armat")

def desarmar_alarma2(mode):
    estat_objectes_casa[f"Alarma_Intrusio_{mode}"][0] = "F"  # Desarmat
    Buzzer.desactiva()
    time.sleep(0.5)
    Buzzer.melodia("to_desarmat")

### Polsadors ### Polsadors ### Polsadors

def detectar_polsadors():
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


                ###### Assignació Diccionaris ######
# diccionaris estàtics
objectes_casa = {
                "Llum_Cuina" : 4,
                "Llum_Passadis" : 2,
                "Llum_Menjador" : 3,
                "Llum_Lavabo" : 5,
                "Llum_Habitacio_1" : 1,
                "Llum_Habitacio_2" : 6,
                "Llum_Habitacio_3" : 13,#7,
                '''"Llum_Servo_R" : ,
                "Llum_Habitació_3" : 7,'''
                
                
              ##@  "Led_WIFI_activat" : LED_WIFI_act,
              ##@  "Led_WIFI_conectat" : LED_WIFI_con,
                ##@"Led_WIFI_comunicant" : LED_WIFI_com,
                
                "Pols_Llum_Cuina" : polsador[0], # Botó teclat 1
                "Pols_Llum_Passadis" : polsador[1], # Botó teclat 5
                "Pols_Llum_Menjador" : polsador[2], # Botó teclat 4
                "Pols_Llum_Lavabo" : polsador[3], # Botó teclat 2
                "Pols_Llum_Habitacio_1" : polsador[4], # Botó teclat 3
                "Pols_Llum_Habitacio_2" : polsador[5], # Botó teclat 6
                "Pols_Llum_Habitacio_3" : polsador[6], # Botó teclat 7
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



                ###### MAIN ######    
estat_objectes_casa["Alarma_Intrusió_Perimetral"] = alarma_2("Perimetral") # Ha de contenir els sensors reed
estat_objectes_casa["Alarma_Intrusió_Total"] = alarma_2("Total") # Ha de contenir els sensors de proximitat i els reed

try:
    while True:
        # Realitza comunicacio
        missatge_rebut = COMs.WIFI_comunicacio(missatge_enviar)
        missatge_enviar = '{}' #els {} s'han de possar si hi ha algun canvi a enviar
        #en la primera versió, es suposa que a cada tecla s'envia el missatge. pero es possible que en altres versions s'enviin ´es canvis en un enviament i en fils
        '''for i in range(16):
            print(i)
            time.sleep(1)
            pca.alterna(i)
        '''
        #print(missatge_rebut)
        
        # Actualitza diccionari si es rebut algun canvi
        if missatge_rebut != '{}':
            diccionari_rebut = to_diccionari(missatge_rebut)

            print("rebut", diccionari_rebut) #########################

            claus_novetat = diccionari_rebut.keys()

            print("clau", claus_novetat)########################

            for key in claus_novetat:
                estat_objectes_casa[key] = diccionari_rebut[key]
                print("estat",estat_objectes_casa[key])
                print("accedint diccionari",objectes_casa[key])
                print("MARC! el index de la llibreria pca9685 es el canal?")
                if "Llum" in key:
                    print("objecte",objectes_casa[key])
                    pca.alterna(objectes_casa[key])
##################################    fer que ejecute los cambios

#########        
        # Diccionari anterior
#       diccionari_estats_anterior = sorted(estat_objectes_casa.items()) # Ordena segons les claus    
#       creació de la variable del diccionari a enviar en mode text
#########
#        apartat 'BBBB
#        capta els valors dels sensors #fer les coses seguint els sensors
#        el diccionari s'actualitza a cada sensor pel que passa
#        així mateix la variable string del diccionari a enviar a la raspberry també s'actualitza
#        # Verificación de estado de la alarma
        
        
#########        
#        if diccionari ara != a abans, entra i canvia coses. Si és el mateix significa que no ha passat res i nno cal q faci res
#        llegeix el diccionari i actualitza l'estat dels actuadors (llums, buzzer, servo...) en funció del nou valor del diccionari que ha aportat el sensor corresponent
#        #el diccionari s'haur``a actualitzat despres de pasar per codi
        
        #codi ignorat fins que funcionin les llums
        '''        
        if estat_objectes_casa["Alarma_Intrusio_Total"][0] == "T": #l'armat Total te prioritat        
            alarma_2("Total")
        elif estat_objectes_casa["Alarma_Intrusio_Perimetral"][0] == "T": #si no esta total comprova si esta perimetral
            alarma_2("Perimetral")
        else:
            alarma_2("Total") #podria ser alarma_2("Perimetral"), tant ne fa pq estan desarmades les dues
        '''
        #print("detectar_polsadors()")
        #detectar_polsadors()
        
        
        missatge_enviar = str(time.time())
        print(missatge_rebut)
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Apagando sistema...")
except Exception as e:
    print(f"Error: {e}")






'''
Arxiu anterior: 
    1-main_BetaPasaPas_20241208.py -> wifi funcions funcional
    2-
    3- 
'''
'''
Accions en aquest ongoing:
    passant a classe
'''
'''

import network
import socket
import time

# Configura l'ESP32 com a punt d'accés
ssid = 'ESP32_AP'
password = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)

print("Punt d'accés actiu")
print("SSID:", ssid)
print("IP:", ap.ifconfig()[0])  # Mostra la IP del punt d'accés

# Configura el servidor TCP de l'ESP32
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.4.1', 12345))  # IP del punt d'accés i port
server_socket.listen(1)

print("Servidor TCP actiu a 192.168.4.1:12345")

# IP de la Raspberry Pi dins de la xarxa ESP32_AP
raspberry_ip = '192.168.4.2'
raspberry_port = 12346  # Port del servidor TCP de la Raspberry Pi

while True:
    try:
        # Com a servidor: escolta i rep missatges de la Raspberry Pi
        print("Esperant connexió de la Raspberry Pi...")

        # Estableix un temps d'espera manual per la connexió
        start_time = time.time()
        conn = None
        while (time.time() - start_time) < 10:  # Temps màxim d'espera: 10 segons
            try:
                conn, addr = server_socket.accept()
                break
            except OSError as e:
                pass  # Cap connexió encara

        if conn is None:
            print("Timeout esperant connexió.")
            continue

        print(f"Connexió establerta amb: {addr}")

        # Rep el missatge
        data = conn.recv(1024).decode('utf-8')
        print(f"Missatge rebut de la Raspberry Pi: {data}")

        conn.close()

        # Com a client: envia missatges a la Raspberry Pi
        print("Connectant com a client al servidor de la Raspberry Pi...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((raspberry_ip, raspberry_port))

        message = "Hola Raspberry"
        client_socket.send(message.encode('utf-8'))
        print(f"Missatge enviat a la Raspberry Pi: {message}")

        client_socket.close()

        time.sleep(1)  # Espera 5 segons abans del següent cicle

    except Exception as e:
        print(f"Error: {e}")
'''