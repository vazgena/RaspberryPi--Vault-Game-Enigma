# sudo apt install python-bluez
# sudo pip3 install paho-mqtt
# sudo pip3 install beacontools
# sudo pip3 install pybluez
# sudo python3 playerTracking.py

from beacontools import BeaconScanner
import requests
import re
from statistics import median_high, mode

bleData = {}
howManyIterations = 1
station = "MTR1"
room = "1"

address = "http://10.255.1.254:8080/bledata"


def callback(bt_addr, rssi, packet, properties):
    try:
        power_val = ''.join([i for i in str(packet) if i.isdigit()])
        upper_number = (int(power_val) / (-1)) - int(rssi)
        lower_number = (10 * 4)
        evaluated_rssi = 10 * (upper_number / lower_number)
        flipped_evaluated_rssi = 100 - evaluated_rssi
        bleData.setdefault(bt_addr, []).append(flipped_evaluated_rssi)
        packet_expanded = str(packet)
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

                    r = requests.post(url=address, data=data)
                    if r.text == "":
                        pass
                    else:
                        pass

                    bleData.pop(bt_addr, None)
            except:
                bleData.pop(bt_addr, None)
        else:
            pass
    except:
        pass


scanner = BeaconScanner(callback)

scanner.start()

while True:
    pass

scanner.stop()
