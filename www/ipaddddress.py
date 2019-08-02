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

import os
from time import sleep
import netifaces as ni
import requests


windows_flag = os.name == 'nt'

if windows_flag:
    # windows
    ni.ifaddresses('{D6C015F8-C4E7-42BB-A8BC-A0D27083C485}')
else:
    #linux
    ni.ifaddresses('eth0')
address = "http://10.255.1.254:8080/ipaddresses"

def loop():
    sleep(30)
    try:
        if windows_flag:
            # windows
            ip = ni.ifaddresses('{D6C015F8-C4E7-42BB-A8BC-A0D27083C485}')[ni.AF_INET][0]['addr']
        else:
            # linux
            ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
        station = "WATCH1WIN"
        data = {'station':station,
                'ip':ip
                }
        r = requests.post(url=address, data=data)
        print(r.text)
        if r.text == "reboot":
            if windows_flag:
                os.system("sudo reboot")
            else:
                os.system("shutdown /r /t 1")
    except:
        pass

while True:
    loop()
