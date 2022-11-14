# simple colour
import plasma
from plasma import plasma_stick
from rgb import *
from time import sleep

NUM_LEDS = 7

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_GRB)

# start updating the LED strip
led_strip.start()

brightness = 0.5

UPDATES = 100 # updates per second

while True:
    count = 0 # count up to 1
    for j in range(0, 100):
        count += 0.01
        if count > 1:
            count = 0
        for i in range(NUM_LEDS):
            led_strip.set_hsv(i, count, 1.0, brightness)
#         sleep(1//UPDATES)
        sleep(0.01)


