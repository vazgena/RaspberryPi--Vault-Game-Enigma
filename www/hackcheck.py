# imports
import serial
from time import sleep
from lxml import html
import requests
import RPi.GPIO as GPIO


# variables
ser = serial.Serial('/dev/ttyUSB0', 9600)
station = "AUD1"
site = "http://10.255.1.254:8080/hackCheck2/"+station

# need to set proper pin on tuesday
pin = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

sleep(10)


def loop():
    try:
        page = requests.get(site)
        tree = html.fromstring(page.content)
        hack = tree.xpath('//div[@id="hack"]/text()')
        try:
            if hack[0] == "clean":
                GPIO.output(pin, GPIO.LOW)
            if hack[0] == "hacked":
                GPIO.output(pin, GPIO.HIGH)
            else:
                GPIO.output(pin, GPIO.LOW)
            hack.clear()
        except:
            pass
    except:
        pass
    sleep(1)


# start
while True:
    loop()

# Reset GPIO settings
GPIO.cleanup()

