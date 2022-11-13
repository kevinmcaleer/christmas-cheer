import rgb
import time
import math 
import urequests
from rgb import *

NUM_LEDS = 7

URL = 'http://api.thingspeak.com/channels/1417/field/2/last.json'
UPDATE_INTERVAL = 120  # refresh interval in secs. Be nice to free APIs!

BRIGHTNESS = 1.0

# How many times the LEDs will be updated per second
UPDATES = 10

from time import time_ns

class Cheerlight():
    
    cheerlights_start = time_ns()
    
    def __init__(self, led_strip):
        self.led_strip = led_strip   
    
    def lights(self):

        # get current time
        self.now = time_ns()
        if self.now - self.cheerlights_start > UPDATE_INTERVAL * 1000:

            # open the json file
            print(f'Requesting URL: {URL}')
            r = urequests.get(URL)
            # open the json data
            j = r.json()
            print('Data obtained!')
            r.close()

            # extract hex colour from the data
            hex = j['field2']

            # and convert it to RGB
            r, g, b = hex_to_rgb(hex)
            
            colour = rgb2hsv(r,g,b)
            print(colour)


            # light up the LEDs
            for i in range(NUM_LEDS):
                self.led_strip.set_hsv(i, colour['hue'], colour['sat'], BRIGHTNESS)

            print(f'LEDs set to {hex}')

            # sleep
            print(f'Sleeping for {UPDATE_INTERVAL} seconds.')
            self.cheerlights_start = time_ns()

class Spin():
    hue = 0
    BRIGHTNESS = 1.0
    
    def __init__(self, led_strip):
        self.led_strip = led_strip
    
    def spinner(self, r,g,b,):
        colour = {'r':r, 'g':g,'b':b}
        c = rgb2hsv(colour['r'],colour['g'],colour['b'])
        for k in range(1,NUM_LEDS):
            for i in range(1,NUM_LEDS):
                
                # check to see if the cycle has started again and blank the last pixel
                if i == 1:
                   self.led_strip.set_hsv(NUM_LEDS-1, 0.0, 0.0, 0.0)
                   self.led_strip.set_hsv(i, c['hue'], c['sat'], BRIGHTNESS)
    #                print(f'i i# {i}')
                else:  
                    self.led_strip.set_hsv(i, c['hue'], c['sat'], BRIGHTNESS)
                
                for j in range(1,i):
                    b = c['val'] / (i * 2 )
                    self.led_strip.set_hsv(j, c['hue'], c['sat'], b)
    #                 print(f'i is {i}, j is {j}')	
                time.sleep(1.0 / UPDATES)

    def cycle(self, count)->int:
        r = 255
        g = 0
        b = 0
        col = rgb2hsv(r,g,b)
        hue = col['hue']
        
        if count < 200:
            hue += 0.01
            if hue == 1: hue = 0
            UPDATES = count
            s = hsv2rgb(hue, col['sat'],col['val'])
            self.spinner(s['red'],s['green'],s['blue'])
            count += 1
        else:
            count = 0
        return count

