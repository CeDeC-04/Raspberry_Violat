from classe_rele import *

rele = Rele(4)

try:
    while True:
        rele.alterna()
        time.sleep(2)
        
except KeyboardInterrupt:
    rele.cleanup()