import Adafruit_DHT
import RPi.GPIO as GPIO
import time

sensor_DHT = 11 

class DHT11:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)  # Mode de numeració de pins com BCM
        GPIO.setup(self.pin, GPIO.IN)  # Configura el pin del PIR com a entrada
        self.sensor = sensor_DHT

    def llegeix_sensor(self):
        f'''Retorna uan llista amb el valor de la temperatura i de la humitat i un missatge'''
        f'''En el cas que alguna de les dues, o ambdues, no s'obtingui una lectura,'''
        f'''es retornarà un None en el valor no obtingut i a la posició 3 un missatge'''
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity is not None and temperature is not None:
            return [temperature, humidity, 'Lectura correcta']
                #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        elif humidity is not None:
            return [None, humidity, 'Error temperatura'] # Ha fallat la lectura de temperatura. Torna-ho a provar
        elif temperature is not None:
            return [temperature, None, 'Error humitat'] # Ha fallat la lectura d'humitat temperatura. Torna-ho a provar
        else:
            return [None, None, 'Error general'] # Ha fallat la lectura. Torna-ho a provar
            #print('Failed to get reading. Try again!')
    
    def llegeix_humitat(self):
        f'''Retorna uan llista amb el valor de la humitat i un missatge'''
        f'''En el cas que no s'obtingui una lectura, es retornarà'''
        f'''un None en la posicició 1 i a la posició 2 un missatge'''
        return [self.llegeix_sensor()[int(i)] for i in '12']

    def llegeix_temperatura(self):
        f'''Retorna uan llista amb el valor de la temperatura i un missatge'''
        f'''En el cas que no s'obtingui una lectura, es retornarà'''
        f'''un None en la posicició 1 i a la posició 2 un missatge'''
        return [self.llegeix_sensor()[int(i)] for i in '02']

    def __str__(self):
        return (f"Classe que retorna una llista on el primer element és la temperatura,"
                f"el segon la humitat i el tercer uan string que dona informació addicional")
        


#return [self.llegeix_sensor()[i] for i in [1, 3]]

'''
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11

pin = 5 # En Mode BCM

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:

    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

else:

    print('Failed to get reading. Try again!')
'''

'''
Mètode Instalacio modul Adafruit_DHT. Extret de https://github.com/adafruit/Adafruit_Python_DHT

sudo apt update

sudo apt install python3-pip

sudo apt install git

sudo python3 -m pip install --upgrade pip setuptools wheel

sudo pip3 install Adafruit_DHT
'''
