import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import subprocess
from time import sleep

debug = 1

# pins
sensor = 'P9_40'
temperatureUp = 'P9_11'
temperatureDown = 'P9_13'

# values that reflect the GPIO input values, initialize system time for button change
upButtonValue = 0
downButtonValue = 0
buttonPressTime = 0
celsius = 0
far = 0

# use subprocess to store IP information in IP_Address
ps = subprocess.Popen(['ip','addr','show'], stdout=subprocess.PIPE)
IP_Address = subprocess.check_output(('grep', 'inet'), stdin=ps.stdout)
ps.wait()
if debug:
    print("System IP Address Information: \n {}".format(IP_Address))

# Use subprocess to store uptime info in UpTimeStr. Parse upTimeStr for exact time.

# Use subprocess to store current date/time.
date = subprocess.check_output(['date'])

ADC.setup()
GPIO.setup(temperatureUp,GPIO.IN)
GPIO.setup(temperatureDown,GPIO.IN)
GPIO.add_event_detect(temperatureUp,GPIO.RISING)
GPIO.add_event_detect(temperatureDown,GPIO.RISING)

while True:
    downPress = False
    upPress = False
    reading = ADC.read(sensor)
    millivolts = reading * 1800  # 1.8V reference = 1800 mV
    celsius = (millivolts - 500) / 10
    far = (celsius * 9/5) + 32
    currentSysTime = subprocess.check_output(['date'])
    print('mv=%d C=%d F=%d' % (millivolts, celsius, far))
    upTimeStr = subprocess.check_output(['uptime'])
    index = upTimeStr.find("up")
    upTime = upTimeStr[index+3:index+11]
    comma = upTime.find(",")
    if comma != -1:
        upTime = upTime[:comma]
    if GPIO.event_detected(temperatureUp):
        upValue = GPIO.input(temperatureUp)
        upPress = True
        upPressTime = subprocess.check_output(['date'])
    if GPIO.event_detected(temperatureDown):
        downValue = GPIO.input(temperatureDown)
        downPress = True
        downPressTime = subprocess.check_output(['date'])
    upValue = GPIO.input(temperatureUp)
    downValue = GPIO.input(temperatureDown)
    with open('/var/www/html/pr3.html','w') as file:
        file.write("<title>Whiskey is Life</title>")
        file.write("<h1>CodyWanKenobi's Jedi Magic</h1>")
        file.write("<P>System IP Information: \n")
        file.write('{}'.format(IP_Address))
        file.write("</P>")
        file.write("<P>Current System Time/Date: ")
        file.write('{}'.format(currentSysTime))
        file.write("</P>")
        file.write("<P>Uptime: ")
        file.write('{}'.format(upTime))
        file.write("</P>")
        if upPress:
            file.write("<P>Up button pressed.</p>\n")

        else:
            file.write("<P>Up button inactive.</p>\n")
        if downPress:
            file.write("<P>Down button pressed.</p>\n")
        else:
            file.write("<P>Down button inactive.</p>\n")
        if upValue:
            file.write("<P>Last Press Temperature Up @: ")
            file.write('{}'.format(upPressTime))
            file.write("</P>")
        if downValue:
            file.write("<P>Last Press Temperature Down @: ")
            file.write('{}'.format(downPressTime))
            file.write("</P>")
        file.write("<P>Temperature (C): ")
        file.write('{}'.format(celsius))
        file.write("</P>")
        file.write("<P>Temperature (F): ")
        file.write('{}'.format(far))
        file.write("</P>")

    sleep(.5)
