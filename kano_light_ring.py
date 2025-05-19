piless_mode_on = False

from datetime import datetime as dt
import time
try:
    from rpi_ws281x import PixelStrip, Color # type: ignore
except:
    print("Running on a non-Pi system. Mocking rpi_ws281x and running with pygame.\nPI-LESS MODE ON")
    piless_mode_on = True
    import pygame
    class Color:

        def __init__(self, r, b, g):
            self.r, self.b, self.g = r, b, g
        def __repr__(self):
            return f"Color({self.r}, {self.b}, {self.g})"

    class Circle:

        def __init__(self, xCoord, yCoord, number):
            self.position = pygame.Vector2(xCoord, yCoord)
            self.number = number

    
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
            easy_circle(color, xCoordinates[n], yCoordinates[n])
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

# x- and y-coordinates for each pixel

xCoordinates = [250, 130, 54, 54, 130, 250, 370, 446, 446, 370]
yCoordinates = [450, 410, 290, 210, 130, 50, 130, 210, 290, 410]
                
import time_functions as tf

# LED ring configuration:
LED_COUNT = 10        # Change this to match the number of LEDs in your ring (24 for Kano ring)
LED_PIN = 18          # GPIO pin (18 works best for PWM on Pi)
LED_FREQ_HZ = 800000  # LED signal frequency
LED_DMA = 10          # DMA channel to use
LED_BRIGHTNESS = 255  # Full brightness (0-255)
LED_INVERT = False    # Needed if using a logic level converter (usually False)
LED_CHANNEL = 0       # Channel for PWM

# initialize strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# colors (R, B, G)
RED = Color(255, 0, 0)
ORANGE = Color(255, 100, 0)
YELLOW = Color(255, 255, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 255, 0)
PURPLE = Color(100, 0, 255)
PINK = Color(255, 0, 255)
WHITE = Color(255, 255, 255)
GRAY = Color(10, 10, 10)

def convertLightNums(num): # 0th light is top, 1st is next one clockwise
    if num <= 9 and num >= 5:
        return num - 5
    if num <= 4 and num >= 0:
        return num + 5

def easy_circle(color, x, y):
    # because i am so lazy
    return pygame.draw.circle(screen, color_rpi_to_pygame(color), pygame.Vector2(x, y), 25)

def color_rpi_to_pygame(rpi):
    r, b, g = rpi.r, rpi.b, rpi.g
    return pygame.Color(r, b, g)

# Function to show a color wipe animation
def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

# Function to set all LEDs to a single color
def solidColor(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def turnOnLightsInRange(rangenum, color):
    for light in range(rangenum):
        strip.setPixelColor(convertLightNums(light), color)
    return

def minutes_to_light():

    # current_minutes = tf.get_minutes()
    current_minutes = 7
    # debugging ^^

    # range of minutes that will turn on those lights
    rangeMax_minutes = 60
    rangeMin_minutes = 54

    range_of_lights_to_turn_on = 10
    
    # if current minutes are not in this range, subtract all of those
    while not current_minutes > rangeMin_minutes or not current_minutes <= rangeMax_minutes:
        rangeMin_minutes -= 6
        rangeMax_minutes -= 6
        range_of_lights_to_turn_on -= 1
        print(f'{rangeMin_minutes}, {rangeMax_minutes}, {range_of_lights_to_turn_on}')
    

    # once the while loop is broken...
    turnOnLightsInRange(range_of_lights_to_turn_on, WHITE)


def hourbinary_to_light():
    binary = tf.hour_to_binary()
    binary_str = str(binary).zfill(4)  # Ensure the binary string is 4 digits
    led_positions = [2, 1, 0, 9]  # Corresponding LED positions for each binary digit
    for i, digit in enumerate(binary_str):
        if digit == '1':
            strip.setPixelColor(led_positions[i], WHITE)
        else:
            strip.setPixelColor(led_positions[i], GRAY)
    emmage = tf.am_or_pm()
    if emmage == 'AM':
        strip.setPixelColor(8, YELLOW)
    else:
        strip.setPixelColor(8, PURPLE)
    return
                
def setAllFakesGray():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, GRAY)
if piless_mode_on == True:
    setAllFakesGray()

scene_num = 0
def change_scene():
    global scene_num
    if scene_num == 2:
        scene_num = 1
        return scene_num
    else:
        scene_num += 1
        return scene_num



# minutes_to_light()
# hourbinary_to_light()
# Example usage
if piless_mode_on == True:
    while running:    
        setAllFakesGray()
        rotation = change_scene()
        if scene_num == 1:
            hourbinary_to_light()
        if scene_num == 2:
            minutes_to_light()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        time.sleep(4)
if piless_mode_on == False:
    try:
        while True:
            rotation = change_scene()
            if rotation == 1:
                hourbinary_to_light()
            if rotation == 2:
                minutes_to_light()
            strip.show()
            time.sleep(4)
    except KeyboardInterrupt:
        solidColor(strip, Color(0, 0, 0))  # Turn off on exit

print("end of the script. :)")