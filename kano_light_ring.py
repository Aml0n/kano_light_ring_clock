from datetime import datetime as dt, date
import time
import time_functions as tf
import openmeteo_requests
import requests_cache
from retry_requests import retry
import csv
import os

try:
    from rpi_ws281x import PixelStrip, Color # type: ignore
    pilessModeOn = False 

except Exception as e:

    print(f"PI-LESS MODE ENABLED: {e}")
    pilessModeOn = True

    import pygame

    ## imitating rpi_ws281x classes and functions in pygame (these are AI generated)

    class Color:

        def __init__(self, r, b, g):
            self.r, self.b, self.g = r, b, g
        def __repr__(self):
            return f"Color({self.r}, {self.b}, {self.g})"
    
    class PixelStrip:

        def __init__(self, num, pin, freq_hz, dma, brightness, invert, channel):
            self.num = num
            self.pixels = [Color(0, 0, 0)] * num
            self.freq_hz = freq_hz
            self.dma = dma
            self.brightness = brightness
            self.invert = invert
            self.channel = channel

        def begin(self):
            print("Initializing mock LED strip.")

        def setPixelColor(self, n, color):
            self.pixels[n] = color
            easyCircle(color, xCoordinates[n], yCoordinates[n])
            print(f"Setting LED {n} to {color}")

        def show(self):
            print("Updated LEDs:", self.pixels)

        def numPixels(self):
            """Return the number of pixels in the display."""
            return len(self)
        
        def __len__(self):
            return self.num
        
    

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    running = True 

    def easyCircle(color, x, y):
    # because i am so lazy
        return pygame.draw.circle(screen, raspColorToPygame(color), pygame.Vector2(x, y), 25)

    def raspColorToPygame(rpi):
        r, b, g = rpi.r, rpi.b, rpi.g
        return pygame.Color(r, b, g)    
    
    # x- and y-coordinates for each pixel

    xCoordinates = [250, 130, 54, 54, 130, 250, 370, 446, 446, 370]
    yCoordinates = [450, 410, 290, 210, 130, 50, 130, 210, 290, 410]


# NOTE to self:
# use 3.13.0 "trying pygame"
# thank you!


# AI generated sections vvvvv
##
##
##

#   # LED ring configuration:
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

# no longer AI generated ^^^^^

gradientColors = [
    (50, 200, 200),
    (68, 213, 168),
    (87, 227, 137),
    (106, 240, 106),
    (125, 220, 75),
    (20, 20, 255),
    (10, 40, 244),
    (20, 80, 233),
    (30, 120, 222),
    (40, 160, 211)
]

# colors (R, B, G)
RED = Color(255, 0, 0)
ORANGE = Color(255, 100, 0)
YELLOW = Color(255, 255, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
PURPLE = Color(100, 0, 255)
PINK = Color(255, 0, 255)
WHITE = Color(255, 255, 255)
GRAY = Color(10, 10, 10)
NEPEACH = Color(200, 50, 50)
NEPEACHDIM = Color(40, 10, 10)
NEORANGE2 = Color(200, 75, 10)
NEYELLOW = Color(175, 100, 10)
NEYELLOWDIM = Color(35, 20, 2)
NEYELLOW2 = Color(150, 125, 10)
NERED = Color(200, 25, 25)
NEMINT2 = Color(125,254,75)
NEMINT2DIM = Color(25, 51, 15)
NETEAL = Color(50,200,200)
NEPURPLE = Color(75,50,250)
NEPURPLE2 = Color(100, 50, 175)
NEPURPLE2DIM = Color(20, 10, 35)
NEPURPLE3 = Color(125, 50, 150)
MOON = Color(95, 95, 95)
OFF = Color(0, 0, 0)

## animations
##
##
##

def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def solidColor(strip, color):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, color)
    strip.show()

def gradientMinutes(rangenum):
    for light in range(rangenum):
        index = convertMinuteNums(light)
        r, g, b = gradientColors[index]
        strip.setPixelColor(index, Color(r, g, b))

    strip.show()
    return

def blinkLight(pixelNumber, pixelColor):
    r, g, b = pixelColor

    time.sleep(0.5)
    strip.setPixelColor(pixelNumber, OFF)
    strip.show()

    time.sleep(0.5)
    strip.setPixelColor(pixelNumber, Color(r, g, b))
    strip.show()
    return

def sunriseSunsetAnimation(stages):
    # stagesFromSunriseUnix would be used as the stages argument here

    now = dt.now()
    nowUnix = int(now.timestamp())

    for num, stage in enumerate(stages):

        if stage == stages[9]:
            strip.setPixelColor(convertFromSunNums(num), NEYELLOW)
            # print(f"{stage}, {nowUnix}, {stages[num + 1]}, {num}")

            moonPosition = getMoonPosition(num)
            strip.setPixelColor(convertFromSunNums(moonPosition), MOON)

            break

        elif stage <= nowUnix and nowUnix < stages[(num + 1)]:

            strip.setPixelColor(convertFromSunNums(num), NEYELLOW) # red is placeholder
            # print(f"{stage}, {nowUnix}, {stages[num + 1]}, {num}")

            moonPosition = getMoonPosition(num)
            strip.setPixelColor(convertFromSunNums(moonPosition), MOON)
            break

## utility
##
##
##

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

def appendCsv(rows):
    with open('savedData/savedSunriseSunset.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

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

        rowsWritten = 0
        rowsDeleted = 0

        for row in reader:
            rowDate = row["date"]
            try:
                rowDateObj = dt.strptime(rowDate, "%Y-%m-%d").date()
                formattedTodayObj = dt.strptime(formattedToday, "%Y-%m-%d").date()
                if rowDateObj >= formattedTodayObj:
                    writer.writerow(row)
                    # print("wrote the row :3")
                    rowsWritten += 1
                else:
                    # print("did NOT write the row")
                    rowsDeleted += 1
            except ValueError:
                print(f"Invalid date format in row: {rowDate}")

    print(f"wrote {rowsWritten} row(s), deleted {rowsDeleted} row(s)")

    with open('savedData/temp.csv', 'r', newline='') as infile, \
         open('savedData/savedSunriseSunset.csv', 'w', newline='') as outfile:
        reader = csv.reader(infile)
        fieldnames = ['date', 'sunriseTime', 'sunsetTime']
        writer = csv.writer(outfile)
        
        writer.writerow(['date', 'sunriseTime', 'sunsetTime'])
        for row in reader:
            # print(row[0])
            writer.writerow(row)

    fileToRemove = "savedData/temp.csv"
    try:
        os.remove(fileToRemove)
        print(f"deleted {fileToRemove}")
    except FileNotFoundError:
        print(f"{fileToRemove} not found")
    except Exception as exception:
        print(f"an error occured: {exception}")

def createSaveFile(): # if the csv doesn't already exist, create it
    try:
        newCSV = open("savedData/savedSunriseSunset.csv", "x")
        newCSV.close()
        print("save file created")

        with open("savedData/savedSunriseSunset.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow("date,sunriseTime,sunsetTime")

        return
    except FileExistsError:
        print("save file already exists")
        return

def convertFromSunNums(pixelNum):
    if pixelNum >= 0 and pixelNum <= 6:
        return pixelNum + 3
    else:
        return pixelNum - 7

def getMoonPosition(sunPosition):
    if sunPosition >= 0 and sunPosition <= 4:
        return sunPosition + 5

    else:
        return sunPosition - 5

def convertMinuteNums(num): # 0th light is top, 1st is next one clockwise
    if num <= 9 and num >= 5:
        return num - 5

    if num <= 4 and num >= 0:
        return num + 5

def minutesToLight():

    currentMinutes = tf.getMinutes()

    # currentMinutes = 59
    # debugging ^^

    startingRangeMaximum = 60
    startingRangeMinimum = 54

    # range of minutes that will turn on those lights
    rangeMaxMinutes = startingRangeMaximum
    rangeMinMinutes = startingRangeMinimum

    rangeLightsOn = 9 # ninth light from top going clockwise; decreases one every loop
    
    # continuously lower the range until the minutes are in the range
    while not currentMinutes > rangeMinMinutes or not currentMinutes <= rangeMaxMinutes:
        rangeMinMinutes -= 6
        rangeMaxMinutes -= 6
        rangeLightsOn -= 1
        # print(f'{rangeMinMinutes}, {rangeMaxMinutes}, {rangeLightsOn}')

    lastLight = convertMinuteNums(rangeLightsOn)
    # print(lastLight) # debug

    # once the while loop is broken...
    gradientMinutes((rangeLightsOn + 1))
    lastLightColor = gradientColors[lastLight]

    # print(lastLightColor) # debug

    for _ in range(4):
        blinkLight(lastLight, lastLightColor)


def hourBinaryToLight():
    binary = tf.hourToBinary()
    binaryStr = str(binary).zfill(4)  # adds zeroes so there are always four digits
    ledPositions = [2, 1, 0, 9]  # Corresponding LED positions for each binary digit
    isAM = tf.isAM()
    for i, digit in enumerate(binaryStr):
        if isAM == True:
            if digit == '1':
                strip.setPixelColor(ledPositions[i], NEYELLOW2)
            else:   
                strip.setPixelColor(ledPositions[i], NEYELLOWDIM)
        else:
            if digit == '1':
                strip.setPixelColor(ledPositions[i], NEPURPLE3)
            else:
                strip.setPixelColor(ledPositions[i], NEPURPLE2DIM)
    if isAM == True:
        strip.setPixelColor(8, NEORANGE2)
    else:
        strip.setPixelColor(8, NEPURPLE)
    return
                
def setAllFakesGray():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, GRAY)

if pilessModeOn == True:
    setAllFakesGray()

sceneNum = 0

def changeScene():
    global sceneNum

    # turns all pixels off between color changes
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))

    if sceneNum == 3:
        sceneNum = 1
        return sceneNum
    else:
        sceneNum += 1
        return sceneNum

sunriseSunsetTimesUnix = sunriseSunset()

sunsetTime = int(sunriseSunsetTimesUnix["sunsetTime"])
sunriseTime = int(sunriseSunsetTimesUnix["sunriseTime"])

sunUpStage = sunriseTime
diffSunsetSunriseSeconds = (sunsetTime - sunriseTime)
sunUpIncrementRounded = round((diffSunsetSunriseSeconds) / 5)
stagesFromSunriseUnix = []

# print(f"{sunsetTime}, {sunriseTime}, {sunUpIncrementRounded}")

for _ in range(5):
    stagesFromSunriseUnix.append(sunUpStage)
    # print(sunUpStage)
    sunUpStage += sunUpIncrementRounded

oneDayInSeconds = 86400
remainingInDaySeconds = (oneDayInSeconds - diffSunsetSunriseSeconds)
sunDownIncrementRounded = round(remainingInDaySeconds / 5)
sunDownStage = sunsetTime

for _ in range(5):
    stagesFromSunriseUnix.append(sunDownStage)
    # print(sunDownStage)
    sunDownStage += sunDownIncrementRounded

# print(stagesFromSunriseUnix)
# print(len(stagesFromSunriseUnix))

if pilessModeOn == True:
    while running:    
        setAllFakesGray()
        rotation = changeScene()
        if sceneNum == 1:
            hourBinaryToLight()
        if sceneNum == 2:
            minutesToLight()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        time.sleep(4)


if pilessModeOn == False:

    try:

        while True: 
            rotation = changeScene()

            if rotation == 1:
                hourBinaryToLight()
                strip.show()
                time.sleep(4)

            if rotation == 2:
                minutesToLight()

            if rotation == 3:
                sunriseSunsetAnimation(stagesFromSunriseUnix)
                strip.show()
                time.sleep(4)

    except KeyboardInterrupt:
        solidColor(strip, 0) # turn off lights
        time.sleep(0.2) # to put some leeway after keyboardinterrupt to properly turn off lights
        strip.show()

print("\nkeyboardinterrupt: end of the script. :)")