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
celsius = ((reading*1800) - 500) / 10
sensor = 'P9_40'
maxTemp = celsius
minTemp = celsius
hourTemperatureList.append(celsius)
dayTemperatureList.append(celsius)
# add another while loop with another timer for every layer added, example: years, decades
while dayTimer < 20:  #86400 seconds is 24 hours
    hourTimer = 0
    listTracker = 0
    avgTempHour = sum(hourTemperatureList)/len(hourTemperatureList)
    dayTemperatureList.append(avgTempHour)
    avgTemp24Hours = sum(dayTemperatureList)/len(dayTemperatureList)
    while hourTimer < 10: # 3600 seconds is 1 hour
        reading = ADC.read(sensor)
        celsius = ((reading*1800) - 500) / 10
        hourTemperatureList.append(celsius)
        #print(celsius)
        #print(hourTemperatureList[listTracker])
        print(minTemp)
        print(maxTemp)
        if hourTemperatureList[listTracker] > maxTemp:
            maxTemp = hourTemperatureList[listTracker]
            #print(maxTemp)
        if hourTemperatureList[listTracker] < minTemp:
            minTemp = hourTemperatureList[listTracker]
            #print(minTemp)
        print('HourAvg=%f DayAvg=%f Min=%f Max=%f' % (avgTempHour, avgTemp24Hours,minTemp,maxTemp ))
        listTracker += 1
        dayTimer += 5
        hourTimer += 5
        sleep(2) #take readings every two minutes
