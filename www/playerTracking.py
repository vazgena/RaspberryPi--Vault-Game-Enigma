#!/usr/bin/env python3
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
from statistics import median_high, mode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from config_station import station, room

bleData = {}
howManyIterations = 1
loop = None

address = "http://10.255.1.254:8080/bleraw"


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
        return 0.89976 * math.pow(ratio, 7.7095) + 0.111


def callback(bt_addr, rssi, packet, properties):
    try:
        packet_expanded = str(packet)
        power_match = re.search('(?<=tx_power: )-?\d+', packet_expanded)
        power_val = None
        if power_match is not None:
            power_str = power_match.group(0)
            power_val = float(power_str)
        rssi_val = float(rssi)

        if "gamine" in packet_expanded:
            try:
                data = {'station': station,
                        'bt_addr': bt_addr,
                        'rssi': rssi_val,
                            'room': room
                }
                if power_val:
                    data['tx_power'] = power_val

                asyncio.run_coroutine_threadsafe(
                    run_execute(requests.post, url=address, data=data), loop)

            except Exception as e:
                print("occured exception in callback -> if gamine", e)
    except Exception as e:
        print("Occured exception in callback ", e)


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
