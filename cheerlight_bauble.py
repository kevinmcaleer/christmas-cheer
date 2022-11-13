# Cheerlight bauble

import WIFI_CONFIG
from network_manager import NetworkManager
import uasyncio
import urequests
from phew import server, connect_to_wifi
from phew.template import render_template
from machine import Pin
import plasma
from plasma import plasma_stick
from time import sleep
import patterns
from patterns import Cheerlight, Spin
from _thread import *

NUM_LEDS = 7

status = "Online"
colour = "#FFFFFF"

# set up the Pico W's onboard LED
pico_led = Pin('LED', Pin.OUT)

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_GRB)

# start updating the LED strip
led_strip.start()

cheer = Cheerlight(led_strip)
spin = Spin(led_strip)

def do_it(led_strip, spin, cheer):
#     global status
    d_lock.acquire()
    s = status
    d_lock.release()
    print(f'thread in background: {s}')
    count = 0
    while True:
#         global status
        d_lock.acquire()
        s = status
        d_lock.release()
        print(f'status: "{s}" count: {count}')
        if s in ['Cheerlights']:
            d_lock.acquire()
            cheer.lights()
            d_lock.release()
        if s in ['Spin']:
            
            print('got Spin')
            spin.cycle(count)
        if s in ['mqtt']:
            patterns.mqtt(led_strip)
        if s in ['Online']:
            if count < 20:
                spin.cycle(count)
                count += 1
            else:
                count = 0
#         sleep(1)

d_lock = allocate_lock()
do_stuff = start_new_thread(do_it,[led_strip, spin, cheer])

def status_handler(mode, status, ip):
    # reports wifi connection status
    print(mode, status, ip)
    print('Connecting to wifi...')
    # flash while connecting
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, 255, 255, 255)
        sleep(0.02)
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, 0, 0, 0)
    if status is not None:
        if status:
            print('Wifi connection successful!')
        else:
            print('Wifi connection failed!')
            
@server.route("/", methods=["GET", "POST"])
def basic(request):
  return render_template("index.html", status=status)

@server.route("/cheerlights", methods=["GET", "POST"])
def cheerlight(request):
    global status
    status = "Cheerlights"
    print(f'status changed to {status}')
    return render_template("index.html", status=status)

@server.route("/mqtt", methods=["GET", "POST"])
def mqtt(request):
    global status
    status = "MQTT"
    print(f'status changed to {status}')
    return render_template("index.html", status=status)

@server.route("/spin", methods=["GET", "POST"])
def spin(request):
    global status
    status = "Spin"
    print(f'status changed to {status}')
    return render_template("index.html", status=status)

# catchall example
@server.catchall()
def catchall(request):
  return "Not found", 404

# set up wifi
try:
    network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
    uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
except Exception as e:
    print(f'Wifi connection failed! {e}')

# start the webserver
server.run()