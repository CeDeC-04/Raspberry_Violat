import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin, min_pulse_width=544, max_pulse_width=2400, default_pulse_width=1500):
        self.pin = pin
        self.min_pulse_width = min_pulse_width
        self.max_pulse_width = max_pulse_width
        self.default_pulse_width = default_pulse_width
        
        # Configurar el GPIO para PWM
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50 Hz (20 ms por ciclo)
        self.pwm.start(0)  # Iniciar PWM con un ciclo de trabajo del 0%
        
        # Establecer la posición inicial
        self.current_position = 0  # Inicializamos en 0 grados o el valor de pulso correspondiente
        self.write(self.default_pulse_width)  # Establecer la posición inicial del servo

    def write(self, value):
        # Si el valor es menor que 200, lo tratamos como un ángulo (0-180 grados)
        if value < 200:
            pulse_width = self.map(value, 0, 180, self.min_pulse_width, self.max_pulse_width)
        else:
            # Si el valor es mayor o igual a 200, lo tratamos como un valor de microsegundos
            pulse_width = value
        
        # Guardar la posición en microsegundos o grados
        self.current_position = self.map(pulse_width, self.min_pulse_width, self.max_pulse_width, 0, 180)
        
        # Convertir el ancho de pulso a un ciclo de trabajo en porcentaje
        duty_cycle = self.pulse_width_to_duty_cycle(pulse_width)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def write_microseconds(self, value):
        # Escribir un valor específico de pulso en microsegundos
        self.current_position = self.map(value, self.min_pulse_width, self.max_pulse_width, 0, 180)
        duty_cycle = self.pulse_width_to_duty_cycle(value)
        self.pwm.ChangeDutyCycle(duty_cycle)
    
    def read(self):
        # Leer la posición actual del servo en grados (0-180)
        return self.current_position
    
    def read_microseconds(self):
        # Leer el valor de pulso en microsegundos basado en la posición actual
        pulse_width = self.map(self.current_position, 0, 180, self.min_pulse_width, self.max_pulse_width)
        return pulse_width
    
    def map(self, x, in_min, in_max, out_min, out_max):
        # Función de mapeo para convertir entre rangos de valores
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def pulse_width_to_duty_cycle(self, pulse_width):
        # Convertir un ancho de pulso en microsegundos a un ciclo de trabajo en porcentaje
        return (pulse_width / 20000.0) * 100
    
    def duty_cycle_to_pulse_width(self, duty_cycle):
        # Convertir un ciclo de trabajo en porcentaje a un ancho de pulso en microsegundos
        return (duty_cycle / 100.0) * 20000

    def detach(self):
        # Detener el control PWM y liberar el pin solo si está iniciado
        if self.pwm is not None:
            self.pwm.stop()
        GPIO.cleanup()  # Limpiar los recursos GPIO
