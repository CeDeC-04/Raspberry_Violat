import RPi.GPIO as GPIO
import time





class Buzzer_Passiu:
    def __init__(self, buzzer_pin, frequencia = 'Sol4'):
        self.notes = notes
        self.pin = buzzer_pin
        GPIO.setmode(GPIO.BCM)  # Mode de numeraciÃ³ de pins
        GPIO.setup(self.pin, GPIO.OUT)  # Configura el pin del buzzer com a sortida

        '''#Definir la freqüencia inicial
        if not (isinstance(frequencia, float) or isinstance(frequencia, int)):
            self.frequencia = notes[frequencia]
        else:
            self.frequencia = frequencia'''
        self.frequencia = self.filtre_nota(frequencia) #Definir la freqüencia inicial
        self.Buzz = GPIO.PWM(self.pin, self.frequencia)

    def nota(self, Frequencia = '', Duty_cycle = 50):
        '''Reprodueix una nota activant el buzzer, però no el desactiva, es queda la nota "in aeternum" /inneternum/'''
        frequencia = self.filtre_nota(Frequencia)
        if frequencia != - 1:
            self.activa(Duty_cycle)
            self.canvia_frequencia(frequencia)
        else:
            self.desactiva()

    def filtre_nota(self, frequencia):
        '''Funció per triar la nota a reproduïr'''
        if not (isinstance(frequencia, float) or isinstance(frequencia, int)):
            try:
                return (notes[frequencia])
            except KeyError:
                return (-1)
        elif frequencia is None:
            return (notes[frequencia])
        else:
            return (frequencia)

    def melodia(self, llista_notes = "to_error"):
        '''Reprodueix una llista de notes (melodia) activant el buzzer, en acabar la llista, atura el buzzer'''
        dd

    def activa(self, Duty_cycle = 50): # Duty cycle al 50% per a millor qualitat de so en la majoria de buzzers
        '''Activa el buzzer per a poder-lo usar'''
        self.Buzz.start(Duty_cycle)

    def desactiva(self):
        '''Atura el buzzer per a que deixi de sonar'''
        self.Buzz.stop()

    def canvia_frequencia(self, frequencia):
        '''Canvia la freqüència de reproducció del buzzer'''
        self.Buzz.ChangeFrequency(frequencia)


    def __str__(self):
        return (f"Funció per a controlar un buzzer passiu amb notes (stribut notes) i melodies (atribut melodies) predefinides\n"
                f"Tot i aquestes notes predefinides, es pot introduir manualment la freqüencia dessitjada per a ser reproduida.\n"
                f"Com a entrada de freqüencia, tant pot ser una variable string amb el nom de la nota predefinida com la frequència\n"
                f"en variable tipus integer o float. Així mateix, la la frequencia de la llista de notes de la melodia pot tenir\n"
                f"exactament el mateix format, o bé str amb el nom del predefinit o el valor int/float indiscriminadament.\n"
                f"Si no s'introdueix cap tipus de frequencia, s'usarà la per defecte Sol4 de 392.00 Hz.")

#### Notes predefinides

notes = {
    "Do0": 16.35, "Do#0": 17.32, "Re0": 18.35, "Re#0": 19.45, "Mi0": 20.60,
    "Fa0": 21.83, "Fa#0": 23.12, "Sol0": 24.50, "Sol#0": 25.96, "La0": 27.50,
    "La#0": 29.14, "Si0": 30.87,
    
    "Do1": 32.70, "Do#1": 34.65, "Re1": 36.71, "Re#1": 38.89, "Mi1": 41.20,
    "Fa1": 43.65, "Fa#1": 46.25, "Sol1": 49.00, "Sol#1": 51.91, "La1": 55.00,
    "La#1": 58.27, "Si1": 61.74,
    
    "Do2": 65.41, "Do#2": 69.30, "Re2": 73.42, "Re#2": 77.78, "Mi2": 82.41,
    "Fa2": 87.31, "Fa#2": 92.50, "Sol2": 98.00, "Sol#2": 103.83, "La2": 110.00,
    "La#2": 116.54, "Si2": 123.47,
    
    "Do3": 130.81, "Do#3": 138.59, "Re3": 146.83, "Re#3": 155.56, "Mi3": 164.81,
    "Fa3": 174.61, "Fa#3": 185.00, "Sol3": 196.00, "Sol#3": 207.65, "La3": 220.00,
    "La#3": 233.08, "Si3": 246.94,
    
    "Do4": 261.63, "Do#4": 277.18, "Re4": 293.66, "Re#4": 311.13, "Mi4": 329.63,
    "Fa4": 349.23, "Fa#4": 369.99, "Sol4": 392.00, "Sol#4": 415.30, "La4": 440.00,
    "La#4": 466.16, "Si4": 493.88,
    
    "Do5": 523.25, "Do#5": 554.37, "Re5": 587.33, "Re#5": 622.25, "Mi5": 659.26,
    "Fa5": 698.46, "Fa#5": 739.99, "Sol5": 783.99, "Sol#5": 830.61, "La5": 880.00,
    "La#5": 932.33, "Si5": 987.77,
    
    "Do6": 1046.50, "Do#6": 1108.73, "Re6": 1174.66, "Re#6": 1244.51, "Mi6": 1318.51,
    "Fa6": 1396.91, "Fa#6": 1479.98, "Sol6": 1567.98, "Sol#6": 1661.22, "La6": 1760.00,
    "La#6": 1864.66, "Si6": 1975.53,
    
    "Do7": 2093.00, "Do#7": 2217.46, "Re7": 2349.32, "Re#7": 2489.02, "Mi7": 2637.02,
    "Fa7": 2793.83, "Fa#7": 2959.96, "Sol7": 3135.96, "Sol#7": 3322.44, "La7": 3520.00,
    "La#7": 3729.31, "Si7": 3951.07,
    
    "Do8": 4186.01, "Do#8": 4434.92, "Re8": 4698.63, "Re#8": 4978.03, "Mi8": 5274.04,
    "Fa8": 5587.65, "Fa#8": 5919.91, "Sol8": 6271.93, "Sol#8": 6644.88, "La8": 7040.00,
    "La#8": 7458.62, "Si8": 7902.13,
    
    "Do9": 8372.02, "Do#9": 8869.84, "Re9": 9397.26, "Re#9": 9956.06,

    None: 1.0, "": -1
}


#### Melodies predefinides

melodies = {
    "alarma_incendis" : ["La7", "Si7", "La7", "Si7", "La7", "Si7", "La7", "Si7", "Do8", "Do8", "Do8", "Do8", "Do8", "Do8", "Do8"],
    "alarma_gas" : ["Do8", "Sol7", "Do8", "Sol7", "Mi7", "Fa7", "Mi7", "Fa7", "Do8", "Do8", "Re8", "Do8", "Do8"],
    "alarma_intrusio" : ["Do8", "Sol8", "Do8", "Sol8", "Do8", "Sol8", "La7", "La7", "Do8", "Do8", "Sol8", "Do8"],
    "to_pulsacio" : ["Sol5", "Do6", "Sol5"],
    "to_armat" : ["Do6", "Mi6", "Sol6"],
    "to_desarmat" : ["Mi5", "Sol5", "Do5"],
    "to_notificacio" : ["Do5", "Fa5", "La5"],
    "to_error" : ["Re5", "Sol5", "Re5"],
    "to_confirmacio" : ["Do6", "Mi6", "Sol6", "Do7"]
    }


'''
# Funció per reproduir una seqüència de notes
def play_sequence(sequence, duration=0.5):
    try:
        pwm.start(1)





    def encendre(self):
        """Activa el buzzer (so)."""
        GPIO.output(self.pin, GPIO.HIGH)
        

    def apagar(self):
        """Desactiva el buzzer (sense so)."""
        GPIO.output(self.pin, GPIO.LOW)
       
    def sonar_durant(self, segons):
        """Fa sonar el buzzer durant un cert temps (en segons)."""
        self.encendre()
        time.sleep(segons)
        self.apagar()

    def cleanup(self):
        """Neteja la configuració de GPIO."""
        GPIO.cleanup()




notes = {
    "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63,
    "F4": 349.23, "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00,
    "A#4": 466.16, "B4": 493.88,
    "C5": 523.25, "C#5": 554.37, "D5": 587.33, "D#5": 622.25, "E5": 659.26,
    "F5": 698.46, "F#5": 739.99, "G5": 783.99, "G#5": 830.61, "A5": 880.00,
    "A#5": 932.33, "B5": 987.77,
    None: 1
}

# Crear PWM
pwm = GPIO.PWM(BUZZER_PIN, 440)  # Freqüència inicial
pwm.start(50)  # Duty cycle al 50%

# Funció per reproduir una seqüència de notes
def play_sequence(sequence, duration=0.5):
    try:
        pwm.start(1)
        for note in sequence:
            if note in notes:
                pwm.ChangeFrequency(notes[note])
                print(f"Tocant {note} - {notes[note]} Hz")
                time.sleep(duration)  # Durada de cada nota
        pwm.stop()
       # GPIO.output(BUZZER_PIN, GPIO.LOW)
       # pwm.ChangeFrequency('1')
    #finally:
    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
        
'''





'''


#####################

        #### Exemple amb un Buzzer Passiu'''
''' Un buzzer passiu necessita una freqüència específica. Amb aquest exemple es generen diferents
 sons.'''
'''    # Importa els mòduls necessaris
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
BUZZER_PIN = 17
GPIO.setup(BUZZER_PIN, GPIO.OUT)
    # Defineix una freqüència (en Hz) i la durada (en segons)
pwm = GPIO.PWM(BUZZER_PIN, 440)  # Freqüència inicial de 440Hz
pwm.start(50)  # Duty cycle al 50%
try:
    pwm.ChangeFrequency(523)  # Nota Do
    time.sleep(0.5)
    pwm.ChangeFrequency(587)  # Nota Re
    time.sleep(0.5)
    pwm.ChangeFrequency(659)  # Nota Mi
    time.sleep(0.5)
    pwm.ChangeFrequency(698)  # Nota Fa
    time.sleep(0.5)
    pwm.stop()
finally:
    GPIO.cleanup()


'''
'''
#####



import RPi.GPIO as GPIO
import time

# Configuració del buzzer
GPIO.setmode(GPIO.BCM)
BUZZER_PIN = 17
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Diccionari de notes i freqüències
notes = {
    "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63,
    "F4": 349.23, "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00,
    "A#4": 466.16, "B4": 493.88,
    "C5": 523.25, "C#5": 554.37, "D5": 587.33, "D#5": 622.25, "E5": 659.26,
    "F5": 698.46, "F#5": 739.99, "G5": 783.99, "G#5": 830.61, "A5": 880.00,
    "A#5": 932.33, "B5": 987.77,
    None: 1
}

# Crear PWM
pwm = GPIO.PWM(BUZZER_PIN, 440)  # Freqüència inicial
pwm.start(50)  # Duty cycle al 50%

# Funció per reproduir una seqüència de notes
def play_sequence(sequence, duration=0.5):
    try:
        pwm.start(1)
        for note in sequence:
            if note in notes:
                pwm.ChangeFrequency(notes[note])
                print(f"Tocant {note} - {notes[note]} Hz")
                time.sleep(duration)  # Durada de cada nota
        pwm.stop()
       # GPIO.output(BUZZER_PIN, GPIO.LOW)
       # pwm.ChangeFrequency('1')
    #finally:
    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
        

# Seqüència de proves
''''''
sequence = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
sequence = ["C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
            "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5"]
play_sequence(sequence, duration=0.5)
''''''
fire_alarm = ["C4", "G4", "C4", "G4"]
sequence = fire_alarm
play_sequence(sequence, duration=0.5)

time.sleep(2)

intrusion_alarm = ["C4", "D4", "E4", "F4", "G4"]
sequence = intrusion_alarm
play_sequence(sequence, duration=0.5)

time.sleep(2)

medical_alarm = ["A4", "A4", '1', "A4", "A4"]
sequence = medical_alarm
play_sequence(sequence, duration=0.5)

time.sleep(2)

gas_alarm = ["F3", '1', "F3", '1']
sequence = gas_alarm
play_sequence(sequence, duration=0.5)

time.sleep(2)

evacuation_alarm = ["A4"]
sequence = evacuation_alarm
play_sequence(sequence, duration=0.5)

time.sleep(2)

custom_alarm = ["C4", "C4", "G4", "G4", "A4", "A4", "G4"]
sequence = custom_alarm
play_sequence(sequence, duration=0.5)'''
