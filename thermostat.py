import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import subprocess
from time import sleep

sensor = 'P9_40'
temperature_up = 'P9_11'
temperature_down = 'P9_13'
ps = subprocess.Popen(['ip addr show | grep inet'], stdout=subprocess.PIPE)
output = subprocess.check_output(('grep', 'process_name'), stdin=ps.stdout)
ps.wait()
print("System IP Address Information: \n {}".format(IP_Address))

ADC.setup()
GPIO.setup(temperature_up,GPIO.IN)
GPIO.setup(temperature_down,GPIO.IN)
while True:
        reading = ADC.read(sensor)
        millivolts = reading * 1800  # 1.8V reference = 1800 mV
        celsius = (millivolts - 500) / 10
        far = (celsius * 9/5) + 32
        print('mv=%d C=%d F=%d' % (millivolts, celsius, far))
        print(GPIO.input(temperature_up))
        print(GPIO.input(temperature_down))
        sleep(1)
