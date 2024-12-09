from machine import Pin
from time import sleep

test  = Pin(33, Pin.OUT)
leds = [Pin(12, Pin.OUT),Pin(14, Pin.OUT), Pin(27, Pin.OUT),Pin(26, Pin.OUT),Pin(25, Pin.OUT),]
pinLector = Pin(23, Pin.IN)

ABCD = 5    #  5     6     7     3     4
BITS = 32   # 32    64   128     8    16
pulsadores = []

def pull():
    for i in range(BITS):
        if  (pinLector.value()) == 1:
            pulsadores.append('1')
        else:
            pulsadores.append('0') 
        for j in range(ABCD):
            leds[j].value((i >> j) & 1)
        
while True:
    pull()
    print (pulsadores)
  
    sleep(0.05)   
    if (pulsadores[0]) == '1':
        test.value()
        
        
    pulsadores = []     
        
        
        
