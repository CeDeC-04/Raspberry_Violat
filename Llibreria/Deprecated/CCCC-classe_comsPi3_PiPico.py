import spidev
import time
import json
from machine import Pin, SPI

class SPIComms:
    def __init__(self, is_master=True, bus=0, device=0, baudrate=50000, mode=0):
        """Inicialitzar la comunicació SPI"""
        self.is_master = is_master
        self.bus = bus
        self.device = device
        self.baudrate = baudrate
        self.mode = mode
        
        if self.is_master:
            # Configurar la Raspberry Pi com a mestre
            self.spi = spidev.SpiDev()
            self.spi.open(self.bus, self.device)
            self.spi.max_speed_hz = self.baudrate
            self.spi.mode = self.mode
        else:
            # Configurar la Raspberry Pi Pico com a esclau
            self.spi = SPI(0, baudrate=self.baudrate, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
            self.cs = Pin(17, Pin.IN, Pin.PULL_UP)  # Pin de selecció de dispositiu (CS)

    def send_data(self, data):
        """Enviar dades des de master a slave"""
        # Convertir el diccionari a JSON i després a bytes
        data_bytes = json.dumps(data).encode('utf-8')
        
        # Enviar les dades
        if self.is_master:
            self.spi.xfer(list(data_bytes))
            print(f"Dades enviades: {data}")
        else:
            print("Aquest mètode només s'ha de cridar des del mestre.")

    def receive_data(self):
        """Rebre dades des de l'esclau al mestre"""
        if self.is_master:
            # Llegir dades des de l'esclau
            response = self.spi.xfer([0] * 64)  # Enviar bytes de petició i rebre la resposta
            message = bytes(response).decode('utf-8')
            try:
                # Convertir la resposta JSON a diccionari
                data_dict = json.loads(message)
                return data_dict
            except ValueError:
                print("Error en la conversió del JSON.")
                return None
        else:
            if not self.cs.value():  # Comprovar si CS està actiu
                message = self.spi.read(64)  # Llegir fins a 64 bytes des del mestre
                message_str = message.decode('utf-8')  # Convertir a text
                try:
                    data_dict = json.loads(message_str)
                    print(f"Diccionari rebut: {data_dict}")
                    # Resposta al mestre
                    self.spi.write(bytearray([0x10, 0x20, 0x30]))  # Exemples de resposta
                except ValueError:
                    print("Error en la conversió del JSON.")

    def close(self):
        """Tancar la connexió SPI"""
        if self.is_master:
            self.spi.close()
