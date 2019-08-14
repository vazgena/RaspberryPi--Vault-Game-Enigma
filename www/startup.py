from threading import Thread
import time
import os


def startprgm(i):
    print ("Running thread %d" % i)
    if (i == 0):
        time.sleep(1)
        print('Running: player tracker')
        os.system("sudo python3 /home/pi/playerTracking.py")
    elif (i == 1):
        print('Running: Ip Tracker')
        time.sleep(1)
        os.system("sudo python3 /home/pi/ipadress.py")
    elif (i == 2):
        print('Running: Ip lighting controller')
        time.sleep(1)
        os.system("sudo python3 /home/pi/color_local.py")
    elif (i == 3):
        print('Running: calibration start')
        time.sleep(1)
        os.system("sudo python3 /home/pi/beacon_calibration.py")
    else:
        pass

for i in range(4):
    t = Thread(target=startprgm, args=(i,))
    t.start()
