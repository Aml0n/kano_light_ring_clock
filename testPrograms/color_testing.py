# this file contains test code to preview color schemes etc

from datetime import datetime as dt
import time
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 10        # Change this to match the number of LEDs in YELLOWour ring (10 for Kano ring)
LED_PIN = 18          # GPIO pin (18 works best for PWM on Pi)
LED_FREQ_HZ = 800000  # LED signal frequencYELLOW
LED_DMA = 10          # DMA channel to use
LED_BRIGHTNESS = 100  # Full brightness (0-255)
LED_INVERT = False    # Needed if using a logic level converter (usuallYELLOW False)
LED_CHANNEL = 0       # Channel for PWM

# initialize strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

BLUE = Color(0, 0, 255)
NEPEACH = Color(200, 50, 50)
NEORANGE2 = Color(200, 75, 10)
NEYELLOW = Color(175, 100, 10)
NEYELLOW2 = Color(150, 125, 10)
NERED = Color(200, 25, 25)
NEMINT2 = Color(125,254,75)
NETEAL = Color(50,200,200)
# NEPURPLE = Color(100,50,250)
# NEPURPLE3 = Color(125, 25, 225)
# NEPURPLE2 = Color(150, 20, 200)

NEPURPLE = Color(75,50,250)
NEPURPLE2 = Color(100, 50, 175)
NEPURPLE2DIM = Color(20, 10, 35)
NEPURPLE3 = Color(125, 50, 150)
N = Color(0, 0, 0)

# strip.setPixelColor(1, NEPURPLE3)
# strip.setPixelColor(2, BLUE)
# strip.setPixelColor(3, NETEAL)
# strip.setPixelColor(4, NEMINT2)
# strip.setPixelColor(5, NERED)
# strip.setPixelColor(6, NEYELLOW2)
# strip.setPixelColor(7, NEYELLOW)
# strip.setPixelColor(8, NEORANGE2)
# strip.setPixelColor(9, NEPURPLE)
# strip.setPixelColor(0, NEPURPLE2DIM)





strip.setPixelColor(9, Color(40, 160, 211))
strip.setPixelColor(8, Color(30, 120, 222))
strip.setPixelColor(7, Color(20, 80, 233))
strip.setPixelColor(6, Color(10, 40, 244))
strip.setPixelColor(5, Color(20, 20, 255))
strip.setPixelColor(4, Color(125, 220, 75))
strip.setPixelColor(3, Color(106, 240, 106))
strip.setPixelColor(2, Color(87, 227, 137))
strip.setPixelColor(1, Color(68, 213, 168))
strip.setPixelColor(0, Color(50, 200, 200))

strip.show()



# colorWipe(strip, N)
# strip.show()