# sudo apt install python-bluez
# sudo pip3 install paho-mqtt
# sudo pip3 install beacontools
# sudo pip3 install pybluez
# sudo python3 playerTracking.py

from beacontools import BeaconScanner
import requests
import re
import os
import sys
import asyncio
import math
from datetime import datetime, timedelta
from statistics import median_high, mode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from config_station import station, room

bleData = {}
bleFilter = {}
bleUpdate = {}
n_iters = 30
howManyIterations = 1
loop = None

address = "http://10.255.1.254:8080/blecalibration"


async def run_execute(function, *args, **kwargs):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda pars, kwpars: function(*pars, **kwpars), args, kwargs)
    return result


def computeDistance(txPower, rssi):
    if rssi == 0:
        return -1  # if we cannot determine accuracy, return -1.

    ratio = rssi / txPower

    if ratio <= 1.0:
        return math.pow(ratio, 10)
    else:
        # return math.pow(ratio, 10)
        return 0.89976 * math.pow(ratio, 9.) + 0.111


class KalmanFilter:
    Q = 1e-5  # process variance
    R = 0.1  # estimate of measurement variance, change to see effect
    max_delta = timedelta(seconds=5)

    def __init__(self, x=-70):
        self.x = x
        self.xhat = x
        self.P = 1.0
        self.xhatminus = None
        self.Pminus = None
        self.K = None
        self.last_update = datetime.now()

    def reinit(self):
        self.xhat = self.x
        self.P = 1.0
        self.xhatminus = None
        self.Pminus = None
        self.K = None

    def check_time(self):
        now = datetime.now()
        if (now - self.last_update) > self.max_delta:
            self.reinit()
        self.last_update = now

    def iter_filter(self, x):
        self.xhatminus = self.xhat
        self.Pminus = self.P + self.Q
        # measurement update
        self.K = self.Pminus / (self.Pminus + self.R)
        self.xhat = self.xhatminus + self.K * (x - self.xhatminus)
        self.P = (1 - self.K) * self.Pminus
        return self.xhat

    def __call__(self, x, *args, **kwargs):
        self.check_time()
        filter_x = self.iter_filter(x)
        return filter_x



def callback(bt_addr, rssi, packet, properties):
    try:
        now = datetime.now()
        rssi_val = float(rssi)

        if rssi_val > -1:
            return

        if bt_addr not in bleFilter:
            bleFilter[bt_addr] = KalmanFilter()
        if bt_addr not in bleUpdate:
            bleUpdate[bt_addr] = now

        if (now - bleUpdate[bt_addr]) < timedelta(seconds=1):
            return

        bleUpdate[bt_addr] = now

        rssi_filter = bleFilter[bt_addr](rssi_val)

        data = {}
        data['station'] = station
        data['bt_addr'] = str(bt_addr)
        data['kalman'] = rssi_filter
        asyncio.run_coroutine_threadsafe(run_execute(requests.post, url=address, data=data), loop)
    except:
        pass


if __name__ == "__main__":

    scanner = BeaconScanner(callback)
    scanner.start()

    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    scanner.stop()
