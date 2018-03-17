from time import sleep
import Adafruit_BBIO.ADC as ADC

#initialize variables
dayTimer = 0
hourTimer = 0
maxTemp = 0
# start at 100 degrees C for minTemp... if this causes an issue in the future, please
# reconsider where your beaglebone is located. It's probably on fire.
minTemp = 100
avgTempHour = 0
avgTemp24Hours = 0
hourTemperatureList = [0]
dayTemperatureList = [0]
listTracker = 0

sensor = 'P9_40'
ADC.setup()
# add another while loop with another timer for every layer added, example: years, decades
while dayTimer < 86400:  #86400 seconds is 24 hours
    hourTimer = 0
    listTracker = 0
    avgTempHour = sum(hourTemperatureList)/len(hourTemperatureList)
    dayTemperatureList.append(avgTempHour)
    avgTemp24Hours = sum(dayTemperatureList)/len(dayTemperatureList)
    while hourTimer < 3600: # 3600 seconds is 1 hour
        reading = ADC.read(sensor)
        celsius = ((reading*1800) - 500) / 10
        hourTemperatureList.append(celsius)
        #print(celsius)
        #print(hourTemperatureList[listTracker])
        print(minTemp)
        if hourTemperatureList[listTracker] > maxTemp:
            maxTemp = hourTemperatureList[listTracker]
        if hourTemperatureList[listTracker] < minTemp:
            minTemp = hourTemperatureList[listTracker]
            print(minTemp)
        #print('HourAvg=%d DayAvg=%d Min=%d Max=%d' % (avgTempHour, avgTemp24Hours,minTemp,maxTemp ))
        listTracker += 1
        dayTimer += 5
        hourTimer += 5
        sleep(5) #take readings every two minutes
