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
site = "http://10.255.1.254:8080/setBackground/"+station+"/"+room

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

################
# # sudo apt-get install arduino -y
# # sudo pip3 install serial
# # sudo apt-get install libxslt-dev

# notes on install
# sudo pkill -f ipadress.py
# sudo pip3 install pyserial
# sudo apt-get update
# sudo apt-get install -y python3-lxml
# sudo pip3 install requests
# sudo rm startup.py
# sudo nano startup.py

# site = "http://10.255.1.254:8080/setBackground/"+station+"/"+room+""
# v = brightness
# r = red Top
# g = green Top
# b = blue Top
# y = yellow Top
# n = no led (black) Top
# l = lower color followed by r/n g/n b/n
# u = upper color custom followed by r/n g/n b/n
################

###########
# sleep(30)
# os.system("echo -n 'v'> /dev/ttyUSB0")
# sleep(10)
# os.system("echo  '50/n'> /dev/ttyUSB0")
# sleep(5)
# os.system("echo -n 'l'> /dev/ttyUSB0")
# sleep(10)
# os.system("echo  '0/n'> /dev/ttyUSB0")
# sleep(2)
# os.system("echo  '0/n'> /dev/ttyUSB0")
# sleep(2)
# os.system("echo  '255/n'> /dev/ttyUSB0")
# sleep(2)
# sleep(10)
# os.system("echo -n 'l'> /dev/ttyUSB0")
# sleep(10)
# os.system("echo  '255/n'> /dev/ttyUSB0")
# sleep(1)
# os.system("echo  '0/n'> /dev/ttyUSB0")
# sleep(1)
# os.system("echo  '0/n'> /dev/ttyUSB0")
# sleep(1)
###########