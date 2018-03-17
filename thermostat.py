import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import subprocess
from time import sleep

debug = 1 # change to 1 for debug statements.

# pins
sensor = 'P9_40'
temperatureUp = 'P9_11'
temperatureDown = 'P9_13'

# values that reflect the GPIO input values
upButtonValue = 0
downButtonValue = 0

# use subprocess to store IP information in IP_Address
ps = subprocess.Popen(['ip','addr','show'], stdout=subprocess.PIPE)
IP_Address = subprocess.check_output(('grep', 'inet'), stdin=ps.stdout)
ps.wait()
if debug:
    print("System IP Address Information: \n {}".format(IP_Address))

# Use subprocess to store uptime info in UpTimeStr. Parse upTimeStr for exact time.
upTimeStr = subprocess.check_output(['uptime'])
index = upTimeStr.find("up")
upTime = upTimeStr[index+3:index+11]
if upTime.find(",") not -1:
    upTime = upTimeStr[index+3:index+10]

if debug:
    print(upTime)

# Use subprocess to store current date/time.
date = subprocess.check_output(['date'])
if debug:
    print("System Date: \n {}".format(date))
ADC.setup()
GPIO.setup(temperatureUp,GPIO.IN)
GPIO.setup(temperatureDown,GPIO.IN)

#update()

# update temperature values and button values
def update():
    while True:
            reading = ADC.read(sensor)
            millivolts = reading * 1800  # 1.8V reference = 1800 mV
            celsius = (millivolts - 500) / 10
            far = (celsius * 9/5) + 32
            print('mv=%d C=%d F=%d' % (millivolts, celsius, far))
            upValue = GPIO.input(temperatureUp)
            downValue = GPIO.input(temperatureDown)
            if debug:
                print(GPIO.input(temperatureUp))
                print(GPIO.input(temperatureDown))

            sleep(1)
