import time
from rpi_ws281x import PixelStrip, Color

# NOTE to self:
# use 3.13.0 "trying pygame"
# thank you!

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

# Example usage
try:
    while True:
        colorWipe(strip, Color(255, 0, 0))  # Red
        colorWipe(strip, Color(0, 255, 0))  # Green
        colorWipe(strip, Color(0, 0, 255))  # Blue
except KeyboardInterrupt:
    solidColor(strip, Color(0, 0, 0))  # Turn off on exit