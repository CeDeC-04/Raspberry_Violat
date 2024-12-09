import time
from machine import Pin, I2C
from classe_pca9685 import PCA9685
from classe_pulsador import Pulsador

# Configuració dels pins I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Ajusta els pins segons el teu maquinari
pulsador = Pulsador(18, False, "pi_pico")

# Inicialitza el controlador PCA9685
pca = PCA9685(i2c)
pca.freq(50)  # Freqüència de 50 Hz per servomotors

# Definim les estances associades als pins
estances = {
    "passadis": 0,
    "cuina": 1,
    "habitacio_1": 2,
    "menjador": 3,
    "habitacio_2": 4,
    "habitacio_3": 5,
    "lavabo": 6
}

# Funció per encendre un pin segons l'estança
def controlar_estanca(estanca, valor_pwm, pausa=1):
    if estanca not in estances:
        print(f"Error: L'estança '{estanca}' no està definida.")
        return

    pin = estances[estanca]
    print(f"Controlant l'estança '{estanca}' al pin {pin} amb valor PWM {valor_pwm}.")
    
    # Encén el canal corresponent amb el valor PWM especificat
    pca.change_duty(pin, valor_pwm)
    time.sleep(pausa)

    # Opcional: apaga el canal després del temps de pausa
    #pca.duty(pin, 0)
    #time.sleep(pausa)

    # Bucle principal que detecta las pulsaciones
# Exemple d'ús
try:
    while True:
        accion = pulsador.gestionar_pulsacions(2)  # Umbral de 1 segundo

        if accion[0] == True:
            #controlar_estanca("cuina", pca.valor[1])
            pca.alterna(0)
            pca.bajando = True
            print(f"valor PWM {pca.valor[0]}.")
            #print(accion)  # Imprimir la acción que se realiza
        elif accion[1] == True:
            pca.bajar_subir(0)
            print(f"valor PWM {pca.valor[0]}.")

        time.sleep(0.1)  # Pequeña espera para evitar sobrecargar el procesador
        
    #controlar_estanca("cuina", 80)  # Controla la cuina amb un valor PWM de 4000
    #time.sleep(2)  # Pausa abans d'encendre una altra estança

except KeyboardInterrupt:
    print("Execució aturada per l'usuari.")
finally:
    # Apaga tots els canals abans de sortir
    for canal in range(16):  # PCA9685 té 16 canals (0-15)
        pca.change_duty(canal, 0)
    print("Tots els canals apagats.")

