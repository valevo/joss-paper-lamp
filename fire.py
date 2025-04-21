
from time import sleep
from rpi_ws281x import *
import argparse


import colorsys as cs
import random

# LED strip configuration:
LED_COUNT      = 30     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 60      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53





# hue goes in 360 degrees, lightness and saturation are percentages
# hue > 60 looks greenn
candle = (255/255, 147/255, 41/255)
# candle_hls = cs.rgb_to_hls(*candle)

# def wrap(orig, add, lower, upper):
#     if add > 0: orig + (add - (upper - orig))
#     add


def flicker(h, l, s):
    i = random.choice((0,1,2))
    if i == 0:
        r = random.randint(a=-5, b=5)
        return min(60, max(0, h + r)), l, s
    elif i ==1: 
        r = random.randint(a=0, b=5)/100
        return h, min(1., max(0.5, l+ +r)), s
    else:
        return h, l, s # don't touch saturation (for now)
    

def fire_(led_strip):
    for r, g, b in led_strip:
        h, l, s = cs.rgb_to_hls(r, g, b)
        new_h, new_l, new_s = flicker(h, l, s)
        yield cs.hls_to_rgb(new_h, new_l, new_s)

def fire(led_strip):
    return list(fire_(led_strip))
    
    # cur_hls = [cs.rgb_to_hls(*v) for v in led_strip]
    # new_hls = [flicker(v) for v in cur_hls]
    # new_rgb = [cs.hls_to_rgb(*v) for v in new_hls]
    # return new_rgb

def unnormalise_rgb(r, g, b):
    return r*255, g*255, b*255

def set_rgb(strip, rgb_ls, normalised=False):
    for i in range(strip.numPixels()):
        cur_c = rgb_ls[i] if not normalised else unnormalise_rgb(*rgb_ls[i])
        strip.setPixelColor(i, Color(*cur_c))
    strip.show()


if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--brightness', help='brightness (0=lowest, 255=brightest')
    parser.add_argument('--numleds', help='number of LEDs to use (144 on the strip)')

    args = parser.parse_args()

    if args.brightness:
        LED_BRIGHTNESS = int(args.brightness)
        assert 0 <= LED_BRIGHTNESS <= 255

    if args.numleds:
        LED_COUNT = int(args.numleds)
        assert 0 <= LED_COUNT <= 144


    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()


    color_ls = [candle]*strip.numPixels()
    set_rgb(strip, color_ls)
    
    while True:

        color_ls = fire(color_ls)
        set_rgb(strip, color_ls)
        sleep(20/1000)
            

    
