import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
from subprocess import call
from time import sleep

sensor = 'P9_40'
temperature_up = 'P9_11'
temperature_down = 'P9_13'
IP_Address = call('ip addr show usb0 | grep inet | grep usb0')
print(IP_Address)

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
