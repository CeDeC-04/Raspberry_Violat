import machine
import time
import re
from classe_WIFI_RaspPI3.py import *
from classe_Buzzer_Passiu import Buzzer_Passiu
from classe_MQ2 import MQ2
import ujson  # Para MicroPython

# Pines para sensores y actuadores
SENSOR_MAG_ventanas = 17
SENSOR_MAG_puerta = 27
SENSORES_IR_PINes = [22, 23, 24, 25]
BUZZER_PIN = 18
SENSOR_MQ2_PIN = 4

# Configuración inicial de sensores y actuadores
buzzer = Buzzer_Passiu(BUZZER_PIN)
sensor_gas = MQ2(SENSOR_MQ2_PIN, platform="pi_pico")
sensor_mag_serie = machine.Pin(SENSOR_MAG_ventanas, machine.Pin.IN, machine.Pin.PULL_UP)
sensor_mag_indep = machine.Pin(SENSOR_MAG_puerta, machine.Pin.IN, machine.Pin.PULL_UP)
sensores_ir = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in SENSORES_IR_PINes]

# Comunicación WiFi
COMs = WIFI()

# Diccionarios de estado
estat_objectes_casa = {
    "Alarma_Intrusio_Perimetral": "FF",  # Estado: Armat(T/F) y Activo(T/F)
    "Alarma_Intrusio_Total": "FF",
    "Alarma_Gas": False,  # True si se detecta gas
}

# Función para verificar sensores
def verificar_sensores(modo):
    if modo == "perimetral":
        return sensor_mag_serie.value() == 0 or sensor_mag_indep.value() == 0
    elif modo == "integral":
        if verificar_sensores("perimetral"):
            return True
        return any(sensor.value() == 0 for sensor in sensores_ir)
    return False

# Función para monitorear el sensor de gas
def verificar_gas():
    if sensor_gas.detecta_particules():
        print("¡Gas detectado!")
        estat_objectes_casa["Alarma_Gas"] = True
        buzzer.melodia("alarma_gas")

# Función principal de la alarma
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

def desarmar_alarma(modo):
    print(f"Alarma desactivada: {modo.upper()}")
    estat_objectes_casa[f"Alarma_Intrusio_{modo.capitalize()}"] = "FF"  # Desarmat y No Activo
    buzzer.melodia("to_desarmat")

# Bucle principal del ESP32
while True:
    try:
        # Recepción de mensajes desde la Raspberry Pi
        missatge_rebut = COMs.WIFI_Comunicacio('{}')
        if missatge_rebut:
            diccionari_rebut = ujson.loads(missatge_rebut)
            estat_objectes_casa.update(diccionari_rebut)

        # Verificación de estado de la alarma
        if estat_objectes_casa["Alarma_Intrusio_Perimetral"][0] == "T":
            alarma("perimetral")
        elif estat_objectes_casa["Alarma_Intrusio_Total"][0] == "T":
            alarma("integral")

    except Exception as e:
        print("Error:", e)
    except KeyboardInterrupt:
        print("Apagando sistema...")
        break
