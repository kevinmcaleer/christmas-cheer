# simple colour
import plasma
from plasma import plasma_stick
from rgb import *

NUM_LEDS = 7


hex = '#00ffff'

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_GRB)

# start updating the LED strip
led_strip.start()

# and convert it to RGB
r, g, b = hex_to_rgb(hex)
hsvcolour = rgb2hsv(r,g,b)
print(f'hsv: {hsvcolour}')

brightness = 0.5

# light up the LEDs
for i in range(NUM_LEDS):
#     led_strip.set_rgb(i, r, g, b)
    led_strip.set_hsv(i, hsvcolour['hue'], hsvcolour['sat'], brightness)

