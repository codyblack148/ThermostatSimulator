from time import sleep
import Adafruit_BBIO.ADC as ADC

#initialize variables
dayTimer = 0
hourTimer = 0
avgTempHour = 0
avgTemp24Hours = 0
hourTemperatureList = []
dayTemperatureList = []
listTracker = 0

sensor = 'P9_40'
ADC.setup()
#initialize temps to first reading
reading = ADC.read(sensor)
celsiusInitial = ((reading*1800) - 500) / 10
sensor = 'P9_40'
maxTemp = celsiusInitial
minTemp = celsiusInitial
hourTemperatureList.append(celsiusInitial)
dayTemperatureList.append(celsiusInitial)
# add another while loop with another timer for every layer added, example: years, decades
while dayTimer < 86400:  #86400 seconds is 24 hours
    hourTimer = 0
    listTracker = 0
    avgTempHour = sum(hourTemperatureList)/len(hourTemperatureList)
    dayTemperatureList.append(avgTempHour)
    avgTemp24Hours = sum(dayTemperatureList)/len(dayTemperatureList)
    with open('/var/www/html/hourlyTempStatistics.html','w') as file:
        file.write("<title>Yes Daddy</title>")
        file.write("<h1>CodyWanKenobi's Jedi Magic</h1>")
        file.write("<P>Current System Temperature Statistics (C): \n")
        file.write('HourAvg=%f DayAvg=%f Min=%f Max=%f' % (avgTempHour, avgTemp24Hours,minTemp,maxTemp ))
        file.write("</P>")
    while hourTimer < 3600: # 3600 seconds is 1 hour
        reading = ADC.read(sensor)
        celsius = ((reading*1800) - 500) / 10
        hourTemperatureList.append(celsius)
        #print(celsius)
        #print(hourTemperatureList[listTracker])
        #print(minTemp)
        #print(maxTemp)
        if hourTemperatureList[listTracker] > maxTemp:
            maxTemp = hourTemperatureList[listTracker]
            #print(maxTemp)
        if hourTemperatureList[listTracker] < minTemp:
            minTemp = hourTemperatureList[listTracker]
            #print(minTemp)
        print('HourAvg=%f DayAvg=%f Min=%f Max=%f' % (avgTempHour, avgTemp24Hours,minTemp,maxTemp ))
        listTracker += 1
        dayTimer += 120
        hourTimer += 120
        sleep(120) #take readings every two minutes
