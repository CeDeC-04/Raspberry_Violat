import RPi.GPIO as GPIO
import time

class Buzzer_Passiu:
    def __init__(self, buzzer_pin):
        self.pin = buzzer_pin
        GPIO.setmode(GPIO.BCM)  # Mode de numeració de pins
        GPIO.setup(self.pin, GPIO.OUT)  # Configura el pin del buzzer com a sortida

    def nota(self, frequencia): 
        GPIO.PWM(self.pin, frequencia).start(100)  # Duty cycle al 50%
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
