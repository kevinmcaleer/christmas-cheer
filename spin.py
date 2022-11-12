# Spin
# makes a spinning effect using a 6 Neopixel circular led strip
# Kevin McAleer
# November 2022

import plasma
from plasma import plasma_stick
import time
from rgb import *

# Set how many LEDs you have
NUM_LEDS = 7

# The SPEED that the LEDs cycle at (1 - 255)
SPEED = 20

# How many times the LEDs will be updated per second
UPDATES = 10

# Set brightness 0.0 to 1.0
BRIGHTNESS = 1.0

# WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)

# Start updating the LED strip
led_strip.start()

offset = 0.0

def spin(r,g,b):
    colour = {'r':r, 'g':g,'b':b}
    c = rgb2hsv(colour['r'],colour['g'],colour['b'])
    for k in range(1,NUM_LEDS):
        for i in range(1,NUM_LEDS):
            
            # check to see if the cycle has started again and blank the last pixel
            if i == 1:
               led_strip.set_hsv(NUM_LEDS-1, 0.0, 0.0, 0.0)
               led_strip.set_hsv(i, c['hue'], c['sat'], BRIGHTNESS)
#                print(f'i i# {i}')
            else:  
                led_strip.set_hsv(i, c['hue'], c['sat'], BRIGHTNESS)
            
            for j in range(1,i):
                b = c['val'] / (i * 2 )
                led_strip.set_hsv(j, c['hue'], c['sat'], b)
#                 print(f'i is {i}, j is {j}')	
            time.sleep(1.0 / UPDATES)
r = 255
g = 0
b = 0
col = rgb2hsv(r,g,b)
hue = col['hue']
while True:
    
    for i in range(4, 500, 2):
        hue += 0.01
        if hue == 1: hue = 0
        UPDATES = i
        s = hsv2rgb(hue, col['sat'],col['val'])
        spin(s['red'],s['green'],s['blue'])