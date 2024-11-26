from lcd_display import lcd
from subprocess import * 
from time import sleep, strftime
from datetime import datetime

lcd = lcd()

cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
temp_cpu = '/usr/bin/vcgencmd measure_temp' # mide la temperatura de la CPU

count = 0

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

while 1:
    lcd.clear()
    ipaddr = run_cmd(cmd)
    temp = run_cmd(temp_cpu)

    lcd.display_string(datetime.now().strftime('%b %d  %H:%M:%S'),1)
    lcd.display_string('IP %s' % ( ipaddr ),2 )
    lcd.display_string('%s' % ( temp ),3 )
    sleep(2)