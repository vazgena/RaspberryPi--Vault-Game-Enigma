# imports
import serial
from time import sleep
from lxml import html
import requests
import os
from random import randrange

# variables
ser = serial.Serial('/dev/ttyUSB0', 9600)


room = "2"
station = "MTR2"
site = "http://10.255.1.254:8080/middlecolor/"+room

sleep(30)

# functions
def loop():
    try:
        col = "n"
        page = requests.get(site)
        tree = html.fromstring(page.content)
        color = tree.xpath('//div[@id="color"]/text()')
        try:
            if color[0] == "red":
                # print("red")
                col = "r"
            if color[0] == "green":
                # print("green")
                col = "g"
            if color[0] == "blue":
                # print("Blue")
                col = "b"
            if color[0] == "yellow":
                # print("yellow")
                col = "y"
            os.system("echo -n '"+col+"' > /dev/ttyUSB0")
            sleep(3)
            os.system("echo -n '" + "n" + "' > /dev/ttyUSB0")
            timers = randrange(3, 7)
            sleep(timers)
            color.clear()
        except:
            pass
    except:
        pass
    sleep(1)

# start
while True:
    loop()
