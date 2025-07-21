import time
from datetime import datetime as dt, date
# import time_functions as tf
import openmeteo_requests
import requests_cache
from retry_requests import retry
import csv
import os

from rpi_ws281x import PixelStrip, Color

def createSaveFile(): # if the csv doesn't already exist, create it
    try:
        newCSV = open("savedData/savedSunriseSunset.csv", "x")
        newCSV.close()
        print("save file created")
        return
    except FileExistsError:
        print("save file already exists")
        return

def deleteOldCache():
    today = date.today()
    formattedToday = today.strftime("%Y-%m-%d")
    # formattedToday = "2025-07-20"
    # todayTimestamp = today.timestamp()
    with open("savedData/savedSunriseSunset.csv", 'r', newline='') as infile, \
         open("savedData/temp.csv", 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['date', 'sunriseTime', 'sunsetTime']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # next(reader, default) # skips header row
        # writer.writeheader()
        for row in reader:
            rowDate = row["date"]
            try:
                rowDateObj = dt.strptime(rowDate, "%Y-%m-%d").date()
                formattedTodayObj = dt.strptime(formattedToday, "%Y-%m-%d").date()
                if rowDateObj >= formattedTodayObj:
                    writer.writerow(row)
                    print("wrote the row :3")
                else:
                    print("did NOT write the row")
            except ValueError:
                print(f"Invalid date format in row: {rowDate}")

    with open('savedData/temp.csv', 'r', newline='') as infile, \
         open('savedData/savedSunriseSunset.csv', 'w', newline='') as outfile:
        reader = csv.reader(infile)
        fieldnames = ['date', 'sunriseTime', 'sunsetTime']
        writer = csv.writer(outfile)
        
        writer.writerow(['date', 'sunriseTime', 'sunsetTime'])
        for row in reader:
            print(row[0])
            writer.writerow(row)

    fileToRemove = "savedData/temp.csv"
    try:
        os.remove(fileToRemove)
        print(f"deleted {fileToRemove}")
    except FileNotFoundError:
        print(f"{fileToRemove} not found")
    except Exception as exception:
        print(f"an error occured: {exception}")

def sunriseSunset():

    createSaveFile()
    deleteOldCache()

    today = date.today()
    formattedToday = today.strftime("%Y-%m-%d")

    timestamps = {}
    rowFound = False

    with open('savedData/savedSunriseSunset.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        while rowFound == False:
            for row in reader:
                if row["date"] == formattedToday:
                    timestamps = row
                    rowFound = True
                    return {"date": row["date"], "sunriseTime": row["sunriseTime"], "sunsetTime": row["sunsetTime"]}

            # if row matching the date isn't found
            csvRows = getSunriseSunsetData()
            appendCsv(csvRows)
            
def appendCsv(rows):
    with open('savedData/savedSunriseSunset.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def getSunriseSunsetData():
    cacheSession = requests_cache.CachedSession('.cache', expire_after = 3600)
    retrySession = retry(cacheSession, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retrySession)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	"latitude": 34.060583399368205,
	"longitude": -118.24431504690445,
	"daily": ["sunset", "sunrise"],
	"timezone": "America/Los_Angeles"
    }   

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0] 
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
    
    daily = response.Daily()
    dailySunset = daily.Variables(0).ValuesInt64AsNumpy()
    dailySunrise = daily.Variables(1).ValuesInt64AsNumpy()
    
    dailyDays = []
    for timestamp in dailySunset:
        dateObj = dt.fromtimestamp(timestamp)
        dailyDays.append(dateObj.strftime("%Y-%m-%d"))

    csvRows = []
    for itemNum in range(len(dailySunset)):
        csvRows.append([dailyDays[itemNum], int(dailySunrise[itemNum]), int(dailySunset[itemNum])])
    return csvRows

    # vvv lots of debugging code

    # print(dailyDays)
    # print(whatDayIsIt)
    # print(dailySunset)
    # print(dailySunrise)
    # print(daily)

# code to figure out increments vvvv

sunriseSunsetTimesUnix = sunriseSunset()

sunsetTime = int(sunriseSunsetTimesUnix["sunsetTime"])
sunriseTime = int(sunriseSunsetTimesUnix["sunriseTime"])

sunUpStage = sunriseTime
diffSunsetSunriseSeconds = (sunsetTime - sunriseTime)
sunUpIncrementRounded = round((diffSunsetSunriseSeconds) / 5)
stagesFromSunriseUnix = []

print(f"{sunsetTime}, {sunriseTime}, {sunUpIncrementRounded}")

for _ in range(5):
    stagesFromSunriseUnix.append(sunUpStage)
    print(sunUpStage)
    sunUpStage += sunUpIncrementRounded

oneDayInSeconds = 86400
remainingInDaySeconds = (oneDayInSeconds - diffSunsetSunriseSeconds)
sunDownIncrementRounded = round(remainingInDaySeconds / 5)
sunDownStage = sunsetTime

for _ in range(5):
    stagesFromSunriseUnix.append(sunDownStage)
    print(sunDownStage)
    sunDownStage += sunDownIncrementRounded

print(stagesFromSunriseUnix)
print(len(stagesFromSunriseUnix))

# ^^^^^^^

LED_COUNT = 10        # Change this to match the number of LEDs in your ring (10 for Kano ring)
LED_PIN = 18          # GPIO pin (18 works best for PWM on Pi)
LED_FREQ_HZ = 800000  # LED signal frequency
LED_DMA = 10          # DMA channel to use
LED_BRIGHTNESS = 15  # Full brightness (0-255)
LED_INVERT = False    # Needed if using a logic level converter (usually False)
LED_CHANNEL = 0       # Channel for PWM

#   # initialize strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

RED = Color(255, 0, 0)
WHITE = Color(255, 255, 255)
OFF = Color(0, 0, 0)
NEYELLOW = Color(175, 100, 10)
MOON = Color(95, 95, 95)

def sunriseSunsetAnimation(stages):
    # stagesFromSunriseUnix would be used as the stages argument here

    now = dt.now()
    nowUnix = int(now.timestamp())

    for num, stage in enumerate(stages):

        if stage == stages[9]:
            strip.setPixelColor(convertToSunNums(num), NEYELLOW)

            moonPosition = getMoonPosition(num)
            strip.setPixelColor(convertToSunNums(moonPosition), MOON)

            break
            # 10th light would turn on

        elif stage <= nowUnix and nowUnix < stages[(num + 1)]:

            strip.setPixelColor(convertToSunNums(num), NEYELLOW) # red is placeholder
            print(f"{stage}, {nowUnix}, {stages[num + 1]}, {num}")

            moonPosition = getMoonPosition(num)
            strip.setPixelColor(convertToSunNums(moonPosition), MOON)
            # this is where the corresponding lights would turn on

            break

def getMoonPosition(sunPosition):

    if sunPosition >= 0 and sunPosition <= 4:
        return sunPosition + 5

    else:
        return sunPosition - 5

# for pixel in range(LED_COUNT):
#     strip.setPixelColor(pixel, OFF)
#     strip.show()

def convertToSunNums(pixelNum):
    if pixelNum >= 0 and pixelNum <= 6:
        return pixelNum + 3
    else:
        return pixelNum - 7

sunriseSunsetAnimation(stagesFromSunriseUnix)
strip.show()

# strip.setPixelColor(convertToSunNums(5), RED)
# strip.show()

# startTime = time.time()
# sunriseSunset()
# endTime = time.time()

# elapsedTime = endTime - startTime
# print(f'ran in {elapsedTime} s')