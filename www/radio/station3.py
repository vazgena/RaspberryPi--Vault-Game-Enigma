 # -20 to 27000


import os
import sys

import Adafruit_ADS1x15
import pygame as pg


from time import sleep
import subprocess
import signal

abc = Adafruit_ADS1x15.ADS1115()

if sys.version_info[:2] <= (2, 7):
    get_input = raw_input
else:
    get_input = input # python3

result = abc.read_adc(0)


pg.mixer.pre_init(44100, -16, 2, 2048)
pg.init()

pg.mixer.music.load('morse.ogg')

perc = 1

pg.mixer.music.play(-1) 
gameloop = True



pg.mixer.music.play()
pg.mixer.music.set_volume(perc)

def percentage(part, whole):
    return 100 * float(part)/float(whole)

while True:
    try:
        result = abc.read_adc(0)
        if result < 23600:
            perc = 0
            print (perc)    

        if result > 23600 and result < 24000:
            newval1 = 24000 - 23600
            newval2 =  result - 23600
            var = percentage(newval2, newval1)
            perc = (var / 100) - .1
            print (perc)


        if result > 24000 and result < 25000:
            perc = 1
            print (perc)

        if result > 25000 and result < 27000:
            newval1 = 27000 - 25000
            newval2 =  result - 25000
            var = percentage(newval2, newval1)
            perc = (((var - 100) / 100) + .2) * -1
            print (perc)

        if result > 27000:
            perc = 0
            print (perc)

        pg.mixer.music.set_volume(perc)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                break
    except AttributeError:
        print AttributeError
pygame.quit()
