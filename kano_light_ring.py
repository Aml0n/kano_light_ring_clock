from datetime import datetime as dt
import time
import time_functions as tf

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
OFF = Color(0, 0, 0)

## animations

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
        index = convertLightNums(light)
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

## utility

def convertLightNums(num): # 0th light is top, 1st is next one clockwise
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

    lastLight = convertLightNums(rangeLightsOn)
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

    if sceneNum == 2:
        sceneNum = 1
        return sceneNum
    else:
        sceneNum += 1
        return sceneNum

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

    except KeyboardInterrupt:
        solidColor(strip, 0) # turn off lights
        time.sleep(0.2) # to put some leeway after keyboardinterrupt to properly turn off lights
        strip.show()

print("end of the script. :)")