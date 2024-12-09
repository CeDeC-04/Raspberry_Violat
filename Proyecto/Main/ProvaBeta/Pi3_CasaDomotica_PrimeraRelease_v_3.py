'''
Arxiu anterior: 
    1-raspberry_bireccional_WIFI_20241129_BetaPasaPas_20241208.py -> amb autodetect
    2-Pi3_CasaDomotica_PrimeraRelease_v_0.py -> funciona, "primera" versió funcional provada amb èxit
    3-Pi3_CasaDomotica_PrimeraRelease_v_2.py -> corregint errors compatibilitat ESP32WROOM_CasaDomotica_PrimeraRelease_MAIN_v_1.py (ESP32)
    4-Pi3_CasaDomotica_PrimeraRelease_v_2.py ->
'''
'''
Accions en aquest ongoing:
    no se q collons poassa q no va
'''

#import socket
#import time
from classe_WIFI_RaspPI3_Beta import *
import re
from classe_teclat4x4_pi3 import *

                ###### Assignació PINs ######
PINs_fila = [10,9,11,5]
PINs_columna = [6,13,19,26]

                ###### Assignació variables ######
missatge_enviar = '{}'            
Tecles = [["Llum_Cuina", "Llum_Lavabo", "Llum_Habitacio_1", "Alarma_Intrusio_Perimetral"], # -> [["1", "2", "3", "A"],
          ["Llum_Menjador", "Llum_Passadis", "Llum_Habitacio_2", "Alarma_Intrusio_Total"], # -> ["4", "5", "6", "B"],
          ["Llum_Habitacio_3", None, None, "Pols_Servo_Obrir"], # -> ["7", "8", "9", "C"],
          [None, "Pols_Timbre", None, "Pols_Servo_Tancar"]] # -> ["*", "0", "#", "D"]]    

    # diccionari dinàmic
estat_objectes_casa = {
                "Llum_Cuina" : "100F", #Pot ser del mínim x% (x) per exemple fins al 100% (100), apagat (F) o encés (T) -> exemple xT 100F
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

                ###### Creació de funcions ######

def to_diccionari(text):
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
                          
                
                
                ###### Creació objectes ######
COMs = WIFI()
Teclat = Teclat4x4(PINs_fila, PINs_columna, Tecles)

COMs.WIFI_reinicia()
                ###### MAIN ######    
try:
    while True:
        
        # Realitza la comunicació amb l'ESP32
        missatge_rebut = COMs.WIFI_comunicacio(missatge_enviar)
##BORRARRRRRRRRRRRRRRR
        if missatge_rebut != '{}':
            print(missatge_rebut) 
        
        missatge_enviar = '{}' #en la primera versió, es suposa que a cada tecla s'envia el missatge. pero es possible que en altres versions s'enviin ´es canvis en un enviament i en fils

        # Actualitza diccionari si es rebut algun canvi
        if missatge_rebut != '{}' and missatge_rebut is not None:
            diccionari_rebut = to_diccionari(missatge_rebut)
            claus_novetat = diccionari_rebut.keys()
            for key in claus_novetat:
                estat_objectes_casa[key] = diccionari_rebut[key]

        # Crea el missatge a enviar, si no hi ha canvis, envia text buit
        clau = Teclat.tecla()
        if clau != None: # Són tots Polsadors
#            print(clau)
            if "Llum" in clau:
#               print("Llum")
                fi = ''
                if estat_objectes_casa[clau][-1] == "F":
                    fi = "T"
                else:
                    fi = "F"
                estat_objectes_casa[clau] = estat_objectes_casa[clau][:-1]+fi
                missatge_enviar = missatge_enviar[:-1]+'"'+clau+f'": "{estat_objectes_casa[clau]}"'+f'{missatge_enviar[len(missatge_enviar)-1]}'#estat_objectes_casa[clau]})' #en la primera versió, es suposa que a cada tecla s'envia el missatge. pero es possible que en altres versions s'enviin ´es canvis en un enviament i en fils
            elif "Intrusio" in clau: # Aquí només armarà o desarmarà l'alarma
#               print("Intrusio")
                ini = ''
                if estat_objectes_casa[clau][0] == "F":
                    ini = "T"
                else:
                    ini = "F"
                estat_objectes_casa[clau] = ini+estat_objectes_casa[clau][-1]
                missatge_enviar = missatge_enviar[:-1]+clau+f': {estat_objectes_casa[clau]}'+f'{missatge_enviar[len(missatge_enviar)-1]}'
                        #estat_objectes_casa[clau]})'#en la primera versió, es suposa que a cada tecla s'envia el missatge. pero es possible que en altres versions s'enviin ´es canvis en un enviament i en fils
            else:
#               print("Iogurt")
                estat_objectes_casa[clau] = not estat_objectes_casa[clau]
                missatge_enviar = missatge_enviar[:-1]+clau+f': {estat_objectes_casa[clau]}'+f'{missatge_enviar[len(missatge_enviar)-1]}'
        #print(missatge_enviar)
        time.sleep(0.01)
        
        
        
        #time.sleep(1)  # Espera 5 segons abans del següent cicle

except socket.timeout:
    print("Timeout esperant connexió.")
except KeyboardInterrupt:
    #print("Inici aturat per l'usuari")
    #COMs.WIFI_tanca()
    #COMs.WIFI_desconecta()
    #COMs.WIFI_scan()
    print("Aturada manual per l'usuari")
except Exception as e:
    print(f"Error: {e}")



'''         
                

while True:
    try:
        # Com a client: envia missatges a l'ESP32
        print("Connectant com a client al servidor de l'ESP32...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((esp_ip, esp_port))

        message = "Hola ESP"
        client_socket.send(message.encode('utf-8'))
        print(f"Missatge enviat a l'ESP32: {message}")

        client_socket.close()

        # Com a servidor: escolta i rep missatges de l'ESP32
        print("Esperant connexió de l'ESP32...")
        server_socket.settimeout(10)  # Timeout per no bloquejar indefinidament
        conn, addr = server_socket.accept()
        print(f"Connexió establerta amb: {addr}")

        # Rep el missatge
        data = conn.recv(1024).decode('utf-8')
        print(f"Missatge rebut de l'ESP32: {data}")

        conn.close()

        time.sleep(1)  # Espera 5 segons abans del següent cicle

    except socket.timeout:
        print("Timeout esperant connexió.")
    except Exception as e:
        print(f"Error: {e}")
        
        
'''








'''
# diccionaris estàtics
objectes_casa = {
             ###   "Llum_Cuina" : Llum_Cuina_PCA,
             ###   "Llum_Passadis" : Llum_Passadis_PCA,
             ###   "Llum_Menjador" : Llum_Menjador_PCA,
             ###   "Llum_Lavabo" : Llum_Lavabo_PCA,
             ###   "Llum_Habitació_1" : Llum_Habitació_1,
             ###   "Llum_Habitació_2" : Llum_Habitació_2,
             ###   "Llum_Habitació_3" : Llum_Habitació_3,
                
             ###   "Led_WIFI_activat" : LED_WIFI_act,
            ###    "Led_WIFI_conectat" : LED_WIFI_con,
             ###   "Led_WIFI_comunicant" : LED_WIFI_com,
                
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
                
            ###    "Proximitat_Passadis" : Proximitat_Passadis,
             ###   "Proximitat_Menjador" : Proximitat_Menjador,
             ###   "Proximitat_Habitacio_2" : Proximitat_Habitacio_2,
              ###  "Proximitat_Habitacio_3" : Proximitat_Habitacio_3,
                
              ###  "Reed_PEntrada" : Reed_PEntrada,
              ###  "Reed_Menjador" : Reed_Menjador,
              ###  "Reed_Habitacio_2" : Reed_Habitacio_2,
              ###  "Reed_Habitacio_3" : Reed_Habitacio_3,
                
                #"Gas_MQ135" : Gas_MQ135, -> 1
                
               ### "Servo_PEntrada" : Servo_PEntrada,
                
                #"Alarma_Gas" : Alarma_Gas, -> 1
               ### "Alarma_Gas" : Gas_MQ135,
               ### "Alarma_Intrusió_Perimetral" : Alarma_Intrusió_Perimetral, # Ha de contenir els sensors reed
               ### "Alarma_Intrusió_Total" : Alarma_Intrusió_Total # Ha de contenir els sensors de proximitat i els reed
                }
'''
