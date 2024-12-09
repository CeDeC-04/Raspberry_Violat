import RPi.GPIO as GPIO
import time

# Uso de la clase Servo
if __name__ == '__main__':
    try:
        servo = Servo(pin=17)  # Suponiendo que el servo está conectado al pin GPIO 17
        
        while True:
            # Movimiento entre 0 y 180 grados en pasos de 10 grados
            for angle in range(0, 180, 10):
                print(f"Moviendo a {angle} grados")
                servo.write(angle)
                time.sleep(1)
            
            # Movimiento inverso de 180 a 0 grados
            for angle in range(180, 0, -10):
                print(f"Moviendo a {angle} grados")
                servo.write(angle)
                time.sleep(1)
    
    except KeyboardInterrupt:
        print("Programa detenido")
        servo.detach()
