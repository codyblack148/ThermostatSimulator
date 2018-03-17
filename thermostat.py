import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import subprocess
from time import sleep

debug = 1 # change to 1 for debug statements.

# update temperature values and button values
def update():
    downPress = False
    upPress = False
    upValue = GPIO.input(temperatureUp)
    downValue = GPIO.input(temperatureDown)
    while True:
            reading = ADC.read(sensor)
            millivolts = reading * 1800  # 1.8V reference = 1800 mV
            celsius = (millivolts - 500) / 10
            far = (celsius * 9/5) + 32
            print('mv=%d C=%d F=%d' % (millivolts, celsius, far))
            if GPIO.event_detected(temperatureUp):
                upValue = GPIO.input(temperatureUp)
                upPress = True
                buttonPressTime = subprocess.check_output(['date'])
                break
            if GPIO.event_detected(temperatureDown):
                downValue = GPIO.input(temperatureDown)
                downPress = True
                buttonPressTime = subprocess.check_output(['date'])
                break
            sleep(1)
    pushToServer(upValue,downValue,buttonPressTime,celsius,far,upPress,downPress)

def pushToServer(x,y,pressTime,c,f,u,d):
    #r = requests.post(url='192.168.7.2:8080',data={'Temperature':celsius},json=None)
    file = open('/var/www/html/pr3.html','w')
    #file.write("#!/usr/bin/python\n")
    #file.write("Content-type: text/html\n\n")
    file.write("<title>Whiskey is Life</title>")
    file.write("<h1>CodyWanKenobi's Jedi Statistics</h1>")
    file.write("<P>This is fun</p>")
    if x:
        file.write("<P>Up button is being pushed now.</p>\n")
    else:
        file.write("<P>Up button is NOT being pushed now.</p>\n")
    if y:
        file.write("<P>Down button is being pushed now.</p>\n")
    else:
        file.write("<P>Down button is NOT being pushed now.</p>\n")
    if u:
        file.write("<P>Last Press Temperature Up @: ")
        file.write('{}'.format(pressTime))
        file.write("</P>")
    if d:
        file.write("<P>Last Press Temperature Down @: ")
        file.write('{}'.format(pressTime))
        file.write("</P>")

    file.write("<P>Uptime: ")
    file.write('{}'.format(upTime))
    file.write("</P>")
    file.write("<P>Temperature (C): ")
    file.write('{}'.format(c))
    file.write("</P>")
    file.write("<P>Temperature (F): ")
    file.write('{}'.format(f))
    file.write("</P>")



    file.close()


    update()

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
upTimeStr = subprocess.check_output(['uptime'])
index = upTimeStr.find("up")
upTime = upTimeStr[index+3:index+11]
comma = upTime.find(",")
if comma != -1:
    upTime = upTime[:comma]

if debug:
    print("System Uptime: {}".format(upTime))

# Use subprocess to store current date/time.
date = subprocess.check_output(['date'])
if debug:
    print("System Date: {}".format(date))
ADC.setup()
GPIO.setup(temperatureUp,GPIO.IN)
GPIO.setup(temperatureDown,GPIO.IN)
GPIO.add_event_detect(temperatureUp,GPIO.BOTH)
GPIO.add_event_detect(temperatureDown,GPIO.BOTH)

pushToServer(upButtonValue,downButtonValue,buttonPressTime,c='fuck me',f='fuck you',u=False,d=False)
