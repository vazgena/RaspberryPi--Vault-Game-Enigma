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
#import math
#import numpy as np
from datetime import datetime, timedelta, time
from statistics import median_high, mode

import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from config_station import station, room

bleData = {}
bleFilter = {}
n_iters = 8
howManyIterations = 1
loop = None

address = "http://10.255.1.254:8080/bledata"
# address = "http://192.168.2.183:8080/bledata"

logging.basicConfig(filename='playerTracking.log',
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info('Logger was configured...')


async def run_execute(function, *args, **kwargs):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda pars, kwpars: function(*pars, **kwpars), args, kwargs)
    return result


# def computeDistance(txPower, rssi):
#     if rssi == 0:
#         return -1  # if we cannot determine accuracy, return -1.
#
#     ratio = rssi / txPower
#
#     if ratio <= 1.0:
#         return np.power(ratio, 10)
#     else:
#         # return math.pow(ratio, 10)
#         return 0.89976 * np.power(ratio, 9.) + 0.111


class KalmanFilter:
    Q = 1e-5  # process variance
    R = 0.1  # estimate of measurement variance, change to see effect
    max_delta = timedelta(seconds=10)

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
        packet_expanded = str(packet)
        power_match = re.search('(?<=tx_power: )-?\d+', packet_expanded)
        if power_match is None:
            return
        power_str = power_match.group(0)
        power_val = float(power_str)
        rssi_val = float(rssi)
        tracker_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        if rssi_val > -1:
            return

        # TODO: hotfix
        power_val = min(power_val, -power_val, -1)
        rssi_val = min(rssi_val, -rssi_val,  -.5)

        if bt_addr not in bleFilter:
            bleFilter[bt_addr] = KalmanFilter()
        if bt_addr not in bleData:
            bleData[bt_addr] = []

        bleData[bt_addr].append(rssi_val)
        if len(bleData[bt_addr]) > n_iters:
            bleData[bt_addr].pop(0)

        rssi_filter = bleFilter[bt_addr](rssi_val)

        window_filter = KalmanFilter(rssi_filter)
        for x in bleData[bt_addr]:
            rssi_window = window_filter(x)

        power_val = -60

        distance = None
        #distance = computeDistance(power_val, rssi_window)

        #if "gamine" in packet_expanded:  # production!!!
        if True:  # for local testing only!!!
            try:
                if len(bleData[bt_addr]) >= howManyIterations:
                    data = {'station': station,
                            'bt_addr': bt_addr,
                            'avg': str(distance),
                            'room': room,
                            'packet_data': str(packet),
                            'properties': str(properties),
                            'rssi': float(rssi),
                            'rssi_window': rssi_window,
                            'rssi_filter': rssi_filter,
                            'tracker_timestamp': tracker_timestamp,
                            }
                    asyncio.run_coroutine_threadsafe(run_execute(requests.post, url=address, data=data), loop)

                    # bleData.pop(bt_addr, None)
            except BaseException as e:
                # bleData.pop(bt_addr, None)
                logging.error('requests.post - bt_addr: {0}, for station: {1}, rssi: {2}', bt_addr, station, rssi)
                logging.exception("Exception: ")
                print(e)
        else:
            pass
    except BaseException as e:
        logging.error('Try callback - packet_expanded: {0} for bt_addr: {1}, rssi: {2}', packet_expanded, bt_addr, rssi)
        logging.exception("Exception: ")

        print(e)


if __name__ == "__main__":

    logging.info('Start playerTracking')
    try:
        scanner = BeaconScanner(callback)
        scanner.start()
        logging.info('Scanner was started')

        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()

        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            logging.exception("Exception: ")
            # pass

        scanner.stop()
        logging.info('Scanner was stopped')

    except ModuleNotFoundError as e:
        logging.error("Scanner error", exc_info=True)

