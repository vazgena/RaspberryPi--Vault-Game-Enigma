# sudo raspi-config enable ssh
# sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
# remove network
# sudo nano ./.bashrc
# change last row
# sudo pip3 install netifaces
# sudo nano /etc/rc.local
# change playerTracking
# (sleep10;python3 ~/startup.py)&
# change name to "eth0" on last row
# sudo cp /lib/udev/rules.d/73-usb-net-by-mac.rules /etc/udev/rules.d/
# sudo apt-get update; sudo apt-get install arduino

import os, ssl
from time import sleep
import paho.mqtt.client as mqttClient

channelLocate = "briansgame/stationip/"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print ("Connected to broker")
        global Connected
        Connected = True
        client.subscribe(channelLocate)
    else:
        print ("Connection failed")


def on_message(client, userdata, message):
    print (message.payload.decode('utf-8'))
    pass


# global variable for the state of the connection
Connected = False
# MQTT conection varibles

broker_address = "mqtt.escapechallenger.com"
mqtt_port = 8083
user = "lassie"
password = "hefr#83v-Stu"
client = mqttClient.Client(client_id="", transport='websockets')
client.username_pw_set(user, password=password)
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, ciphers=None)
client.connect(broker_address, mqtt_port, 60)  # connect to broker
client.loop_start()  # start the loop

while not Connected:  # Wait for connection
    sleep(.5)

def loop():
    sleep(30)



while True:
    loop()
