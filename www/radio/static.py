 # -20 to 27000


import os
import sys

import Adafruit_ADS1x15
import pygame as pg


from time import sleep


abc = Adafruit_ADS1x15.ADS1115()

if sys.version_info[:2] <= (2, 7):
    get_input = raw_input
else:
    get_input = input # python3

result = abc.read_adc(0)


pg.mixer.pre_init(44100, -16, 2, 2048)
pg.init()

pg.mixer.music.load('static.mp3')

perc = 1

pg.mixer.music.play(-1) 
gameloop = True



pg.mixer.music.play()
pg.mixer.music.set_volume(perc)

def percentage(part, whole):
    return 100 * float(part)/float(whole)

while True:
    result = abc.read_adc(0)
    print result
    if result < 11800:
        perc = 1
        print perc 
    
    if result > 11800 and result < 12800:
        newval1 = 12800 - 11800
        newval2 =  result - 11800
        var = percentage(newval2, newval1)
        perc = (((var - 100) / 100) + .2) * -1 
        print perc

    if result > 12800 and result < 13600:
        perc = 0
        print perc
    
    #play station 1
    
    if result > 13600 and result < 14600:
        newval1 = 14600 - 13600
        newval2 =  result - 13600
        var = percentage(newval2, newval1)
        perc = (var / 100) - .1
        print perc

    if result > 14600 and result < 18600:
        perc = 1
        print perc


    if result > 18600 and result < 19600:
        newval1 = 16600 - 14600
        newval2 =  result - 14600
        var = percentage(newval2, newval1)
        perc = (((var - 100) / 100) + .2) * -1 
        print perc

    if result > 19600 and result < 20600:
        perc = 0
        print perc

    #play station 2
    if result > 20600 and result < 22600:
        newval1 = 22600 - 20600
        newval2 =  result - 20600
        var = percentage(newval2, newval1)
        #print var
        perc = (((var) / 100) - .2)
        print perc
    
    if result > 20600 and result < 22600:
        perc = 1
        print perc

    if result > 22600 and result < 24000:
        newval1 = 24000 - 22600
        newval2 =  result - 22600
        var = percentage(newval2, newval1)
        perc = (((var - 100) / 100)) * -1
        print perc

    if result > 24000 and result < 25000:
        perc = 0
        print perc

    #play station 3
    if result > 25000 and result < 27000:
        newval1 = 27000 - 25000
        newval2 =  result - 25000
        var = percentage(newval2, newval1)
        #print var
        perc = (((var) / 100) - .2)
        print perc
    
    if result > 27000:
        perc = 1
        print perc

    pg.mixer.music.set_volume(perc)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            break
            
pygame.quit()

    #$sleep(.1)



