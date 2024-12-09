import ustruct
import time

class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.state = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        self.valor = [100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]  # Valor inicial
        self.bajando = True  # Empezamos bajando
        self.reset()

    def _write(self, address, value):
        self.i2c.writeto_mem(self.address, address, bytearray([value]))

    def _read(self, address):
        return self.i2c.readfrom_mem(self.address, address, 1)[0]

    def reset(self):
        self._write(0x00, 0x00)  # Mode1

    def freq(self, freq=None):
        if freq is None:
            return int(25000000.0 / 4096 / (self._read(0xfe) - 0.5))
        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode = self._read(0x00)  # Mode 1
        self._write(0x00, (old_mode & 0x7F) | 0x10)  # Mode 1, sleep
        self._write(0xfe, prescale)  # Prescale
        self._write(0x00, old_mode)  # Mode 1
        time.sleep_us(5)
        self._write(0x00, old_mode | 0xa1)  # Mode 1, autoincrement on

    def pwm(self, index, on=None, off=None):
        if on is None or off is None:
            data = self.i2c.readfrom_mem(self.address, 0x06 + 4 * index, 4)
            return ustruct.unpack('<HH', data)
        data = ustruct.pack('<HH', on, off)
        self.i2c.writeto_mem(self.address, 0x06 + 4 * index, data)

    def duty(self, index, value=None, invert=False):
        if value is None:
            pwm = self.pwm(index)
            if pwm == (0, 4096):
                value = 0
            elif pwm == (4096, 0):
                value = 4095
            value = pwm[1]
            if invert:
                value = 4095 - value
            return value
        if not 0 <= value <= 4095:
            raise ValueError("Out of range")
        if invert:
            value = 4095 - value
        if value == 0:
            self.pwm(index, 0, 4096)
        elif value == 4095:
            self.pwm(index, 4096, 0)
        else:
            self.pwm(index, 0, value)

    def change_duty(self, index, value=None, invert=False):
        """Modifica el ciclo de trabajo en un índice dado."""
        self.valor[index] = value
        duty_value = int(self.valor[index] * 40.95)
        self.duty(index, duty_value, invert)
        self.state[index] = True
        
    def alterna(self, index):
        if self.state[index]:
            self.duty(index, 0)
            self.state[index] = False
        else:
            duty_value = int(self.valor[index] * 40.95)
            self.duty(index, duty_value)
            self.state[index] = True

    def bajar_subir(self, index):
        """Función integrada para manejar el descenso y ascenso del valor y cambiar el ciclo de trabajo."""
        if self.bajando and self.valor[index] >= 1:
            self.valor[index] -= 5
            if self.valor[index] <= 1:
                self.valor[index] = 1
                self.bajando = False
        else:
            self.valor[index] += 5
            if self.valor[index] >= 100:
                self.valor[index] = 100
                self.bajando = True
        
        self.change_duty(index, self.valor[index])
