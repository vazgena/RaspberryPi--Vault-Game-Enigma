import os
import time
import re
from random import sample
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from pymysql import InternalError, connect, cursors
from random import choice
import numpy as np
from scipy.spatial.distance import cdist

import requests

from base_update_script import update_rows


# Variables
app = Flask(__name__)
dbuser = 'game'
dbpass = 'h95d3T7SXFta'


# Basic connection for the database
def data_connect():
    return connect(
        db='game',
        user=dbuser,
        passwd=dbpass,
        host='localhost',
        autocommit=True)


def test_timer():
    atkroom = '2'
    itemID = '8'
    query = "INSERT INTO marketOwned (itemID, text, numberOwned, team) VALUES (%s, %s, %s, %s);"
    connection = data_connect()
    c = connection.cursor()
    c.execute(query, (itemID, "", "1", atkroom))
    connection.close()


def test_hach3():
    connection = data_connect()
    c = connection.cursor()
    room = '2'

    if str(room) == "1":
        atkroom = "2"
    if str(room) == "2":
        atkroom = "1"

    room_list_sql = "SELECT stationList.* FROM stationList LEFT JOIN  hackCheck ON stationList.name=hackCheck.roomstation " \
                    "WHERE stationList.room = %s AND (hackCheck.status NOT LIKE 'hacked' OR hackCheck.status IS NULL);"
    c.execute(room_list_sql, atkroom)
    room_list = list(c.fetchall())

    hack_count_check = 'SELECT * FROM hacks WHERE team = %s'
    c.execute(hack_count_check, str(room))
    hack_count_sql = list(c.fetchall())
    how_many_hacks = 0
    how_much_time = 60

    for i in hack_count_sql:
        how_many_hacks = i[2]

    if len(room_list) < 4:
        # Select All
        stations_hack = room_list
        print(len(room_list))
    else:
        stations_hack = sample(room_list, 3)
    for station in stations_hack:
        station_name = station[1]
        hack_stations = 'INSERT INTO hackCheck (roomstation, status, timeRemaining) VALUES (%s, %s, %s)'
        c.execute(hack_stations, (station_name, "hacked", how_much_time))
        funding1 = "INSERT INTO hacks (team, howMany) VALUES (%s, %s) ON DUPLICATE KEY UPDATE team = %s, howMany = %s;"
        c.execute(funding1, (room, int(how_many_hacks) - 1, room, int(how_many_hacks) - 1))
    connection.close()


def test_fake_bomb():
    connection = data_connect()
    c = connection.cursor()
    room = 1
    if str(room) == "1":
        atkroom = "2"
    if str(room) == "2":
        atkroom = "1"
    sql_query = "INSERT INTO bombsDeployed (room, fake_bomb, stationName, timeDeployed) VALUES (%s,TRUE, %s, %s);"
    c.execute(sql_query, (atkroom, '', datetime.now() + timedelta(seconds=31)))
    connection.close()


def test_hach_market():
    connection = data_connect()
    c = connection.cursor()

    getTableListSQL = 'SELECT * FROM market WHERE id=29;'
    c.execute(getTableListSQL)
    marketAvailableList = list(c.fetchall())
    i = marketAvailableList[0]
    marketText = re.sub(r"(?<!\\)'", "\\'", i[1])
    marketCost = i[2]
    marketMultiple = i[3]
    marketID = i[0]

    getTableListSQL = 'SELECT * FROM marketCurrent ORDER BY RAND() LIMIT 1;'
    c.execute(getTableListSQL)
    marketCur = list(c.fetchall())

    fixes = [
        ('marketCurrent', marketCur[0][0], ('text', 'cost', 'itemID', 'multipleAllowed'), (marketText, marketCost, marketID, marketMultiple)),
        ]
    update_rows(c, fixes)

    connection.close()


def test_audio_volume():
    connection = data_connect()
    c = connection.cursor()
    room = 2
    play_add_sql = "INSERT INTO audiomanager (whattoplay, room) VALUES (%s, %s)"
    c.execute(play_add_sql, ("gamewon", room))

    connection.close()


def test_track_log():
    connection = data_connect()
    c = connection.cursor(cursor=cursors.SSCursor)
    date_trash_left = datetime.strptime("2019-07-26 22:16:00,000", "%Y-%m-%d %H:%M:%S,%f")
    date_trash_rigth = date_trash_left + timedelta(minutes=100)

    sql_request = "SELECT * FROM log_tracker " \
                  "LEFT JOIN stationList ON log_tracker.station=stationList.name " \
                  "WHERE timestamp > %s AND timestamp < %s ORDER BY log_tracker.timestamp ASC;"
    try:
        c.execute(sql_request, (date_trash_left, date_trash_rigth))
        rows = c.fetchall_unbuffered()
        prev_time = None

        for row in rows:
            cur_time = row[5]
            if prev_time:
                time_delta = cur_time - prev_time
                # time.sleep(time_delta.total_seconds()/2)
            prev_time = cur_time
            station = row[2]
            bt_addr = row[1]
            avg = str(row[4])
            room = row[8]
            data = {
                'station': station,
                'bt_addr': bt_addr,
                'avg': avg,
                'room': room
            }
            print(row[5])
            response = requests.post("http://127.0.0.1:8080/bledata", data=data)
            a = 1
    except:
        connection.close()



locations_room = {}

def init_locations():
    connection = data_connect()
    c = connection.cursor()
    for room in [1, 2]:
        select_locations_sql = "SELECT * FROM station_position WHERE room=%s;"
        c.execute(select_locations_sql, room)
        list_locations = list(c.fetchall())
        list_stations = []
        locations = np.zeros((len(list_locations), 2))
        for i, location in enumerate(list_locations):
            list_stations.append(location[2])
            locations[i, :] = [location[3], location[4]]
        locations_room[room] = {
            "locations": locations,
            "stations": list_stations
        }
    connection.close()


def test_trilateration():
    init_locations()
    n_step = 60
    k = 1.1
    while True:
        room = choice((1, 2))
        time_start = time.time()
        locations = locations_room[room]['locations']
        x = np.random.random() * locations.max(axis=0)[0]
        y = np.random.random() * locations.max(axis=0)[1]
        point = np.array([[x, y]])
        print(x, y)
        dists = cdist(point, locations)[0, :]
        min_dist_i = np.argmin(dists)
        print(locations_room[room]['stations'][min_dist_i], dists[min_dist_i])
        while time_start + n_step > time.time():
            for i, dist in enumerate(dists):
                try:
                    station = locations_room[room]['stations'][i]
                    data = {'station': station,
                            'bt_addr': "asd3234f-{}".format(room),
                            'avg': str(dist*k),
                            'room': room,
                            }
                    address = "http://127.0.0.1:8080/bledata"
                    response = requests.post(url=address, data=data)
                except:
                    pass


def test_beacons_pair():
    init_locations()
    n_step = 60
    k = 1.1

    # for Gaussian distribution
    mu = 0  # unbiased
    sigma = 2  # ft.
    dx = 0.3  # ft. bias of back beacon

    macs = ["80:7d:3a:b7:70:ee", "30:ae:a4:27:ff:36"]

    # mySQL work presets
    connection = data_connect()
    c = connection.cursor()
    insert_trackers_value_sql = "INSERT INTO trackers_value " \
                 "(mac, station, value, tracker_timestamp) " \
                 "VALUES " \
                 "(%s, %s, %s, %s), " \
                 "(%s, %s, %s, %s);"
    update_trackers_sql = "INSERT INTO trackers (macstat, mac, station, signal_avg, room) " \
                          "VALUES (%s, %s, %s, %s, %s) "\
                          "ON DUPLICATE KEY UPDATE " \
                          "macstat = %s, mac = %s, station = %s, signal_avg = %s, room = %s, timestamp = %s;"

    while True:
        # room = choice((1, 2))  # uniform!
        room = 1
        time_start = time.time()
        locations = locations_room[room]['locations']

        # room coordinates
        x_min = 0
        y_min = 0
        x_max = locations.max(axis=0)[0]
        y_max = locations.max(axis=0)[1]
        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2

        # use unbiased Gaussian distribution
        x = np.random.normal(mu, sigma, 2) + x_mid
        y = np.random.normal(mu, sigma, 2) + y_mid

        point1 = np.array([[x[0], y[0]]])
        point2 = np.array([[x[1] + dx, y[1]]])
        print(point1, point2)

        dists1 = cdist(point1, locations)[0, :]
        dists2 = cdist(point2, locations)[0, :]

        min_dist_i_1 = np.argmin(dists1)
        min_dist_i_2 = np.argmin(dists2)

        print("Front beacon: " + locations_room[room]['stations'][min_dist_i_1], dists1[min_dist_i_1])
        print("Back beacon: " + locations_room[room]['stations'][min_dist_i_2], dists2[min_dist_i_2])

        while time_start + n_step > time.time():
            for i, dist1, dist2 in zip(range(len(dists1)), dists1, dists2):
                try:
                    avg1 = float(dist1*k)
                    avg2 = float(dist2*k)

                    station = locations_room[room]['stations'][i]
                    ts = time.time()
                    tracker_timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                    # renew trackers list
                    # front
                    macstat = str(macs[0]) + "," + str(station)
                    c.execute(update_trackers_sql, (macstat, macs[0], station, avg1, room,
                                                    macstat, macs[0], station, avg1, room, tracker_timestamp))
                    # back
                    macstat = str(macs[1]) + "," + str(station)
                    c.execute(update_trackers_sql, (macstat, macs[1], station, avg2, room, macstat,
                                                    macs[1], station, avg2, room, tracker_timestamp))

                    # trackers_value
                    c.execute(insert_trackers_value_sql,
                              (macs[0], station, avg1, tracker_timestamp,  # front (C1)
                               macs[1], station, avg2, tracker_timestamp))  # back (C2)
                except Exception as e:
                    print('test_beacons_pair(): ' + str(e))
                    # pass
        c.fetchall()


if __name__ == "__main__":
    # test_audio_volume()
    # test_fake_bomb()
    # test_track_log()
    # test_trilateration()
    test_beacons_pair()
