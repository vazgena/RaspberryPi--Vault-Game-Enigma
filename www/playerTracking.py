# sudo apt install python-bluez
# sudo pip3 install paho-mqtt
# sudo pip3 install beacontools
# sudo pip3 install pybluez
# sudo python3 playerTracking.py

from beacontools import BeaconScanner
import requests
import re
import sys
import asyncio
from statistics import median_high, mode

bleData = {}
howManyIterations = 1
station = "MKP1"
room = "1"
loop = None

address = "http://10.255.1.254:8080/bledata"


async def run_execute(function, *args, **kwargs):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda pars, kwpars: function(*pars, **kwpars), args, kwargs)
    return result


def computeDistance(txPower, rssi):
    pass


def callback(bt_addr, rssi, packet, properties):
    try:
        power_val = ''.join([i for i in str(packet) if i.isdigit()])
        upper_number = (int(power_val) / (-1)) - int(rssi)
        lower_number = (10 * 4)
        evaluated_rssi = 10 * (upper_number / lower_number)
        flipped_evaluated_rssi = 100 - evaluated_rssi
        bleData.setdefault(bt_addr, []).append(flipped_evaluated_rssi)
        packet_expanded = str(packet)

        distance = computeDistance(float(power_val)*(-1), float(rssi))

        if "gamine" in packet_expanded:
            try:
                if len(bleData[bt_addr]) >= howManyIterations:
                    # send Data to server
                    avg = 0
                    #for j in bleData[bt_addr]:
                    #    if int(j) > int(avg):
                    #       avg = int(j)
                    try:
                        avg = mode(bleData[bt_addr])
                    except:
                        avg = median_high(bleData[bt_addr])
                    tx_amount = re.findall(r'\d+', packet_expanded)
                    data = {'station': station,
                           'bt_addr': bt_addr,
                           'avg': str(avg),
                           'room': room,
                            'packet_data': str(tx_amount[0]),
                            'properties': str(properties)
                            }

                    asyncio.run_coroutine_threadsafe(run_execute(requests.post, url=address, data=data), loop)

                    bleData.pop(bt_addr, None)
            except:
                bleData.pop(bt_addr, None)
        else:
            pass
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
