import os
import re
import json
from datetime import datetime, timedelta
import matplotlib
from matplotlib import pyplot as plt
from pymysql import InternalError, connect, cursors
import asyncio
import concurrent.futures

import numpy as np
import scipy.signal

dbuser = 'game'
dbpass = 'h95d3T7SXFta'

def data_connect():
    return connect(
        db='game',
        user=dbuser,
        passwd=dbpass,
        host='localhost',
        autocommit=True)


def get_data(track_name, room=1, show=False):
    connection = data_connect()
    con = connection.cursor(cursor=cursors.SSCursor)
    # con = connection.cursor()
    date_trash_left = datetime.strptime("2019-07-26 22:10:00,000", "%Y-%m-%d %H:%M:%S,%f")
    date_trash_rigth = date_trash_left + timedelta(minutes=100)

    sql_request = "SELECT log_tracker.volume, log_tracker.station, log_tracker.timestamp FROM log_tracker " \
                  "LEFT JOIN TrackerNames on log_tracker.mac=TrackerNames.mac " \
                  "LEFT JOIN stationList ON log_tracker.station=stationList.name " \
                  "WHERE stationList.room=%s AND TrackerNames.name=%s AND log_tracker.timestamp > %s AND log_tracker.timestamp < %s ORDER BY log_tracker.timestamp ASC;"
    con.execute(sql_request, (room, track_name, date_trash_left, date_trash_rigth))

    rows = con.fetchall_unbuffered()
    # rows = con.fetchall()

    volume_dict = {}
    time_dict = {}

    for row in rows:
        station = row[1]
        value = row[0]
        date = row[2]
        if station not in volume_dict:
            volume_dict[station] = []
            time_dict[station] = []
        volume_dict[station].append(value)
        time_dict[station].append(date)

    if len(time_dict) == 0:
        return

    fig, ax = plt.subplots()

    for key in volume_dict:
        x = scipy.signal.medfilt(np.array(volume_dict[key]), kernel_size=(3,))
        y = time_dict[key][:len(x)]
        ax.plot(y, x, label=key, marker='.')

    # fig.xlabel('x label')
    # fig.ylabel('y label')

    ax.set_title("%s_%s" % (track_name, room))

    ax.legend()
    if not show:
        fig.savefig('./data/track_%s_%s.png' % (track_name, room), quality=100, dpi=900)
    else:
        plt.show()


def get_data_all(track_name, show=False):
    connection = data_connect()
    con = connection.cursor(cursor=cursors.SSCursor)
    # con = connection.cursor()
    date_trash_left = datetime.strptime("2019-07-26 22:10:00,000", "%Y-%m-%d %H:%M:%S,%f")
    date_trash_rigth = date_trash_left + timedelta(minutes=100)

    sql_request = "SELECT log_tracker.volume, log_tracker.station, log_tracker.timestamp FROM log_tracker " \
                  "LEFT JOIN TrackerNames on log_tracker.mac=TrackerNames.mac " \
                  "LEFT JOIN stationList ON log_tracker.station=stationList.name " \
                  "WHERE TrackerNames.name=%s AND log_tracker.timestamp > %s AND log_tracker.timestamp < %s ORDER BY log_tracker.timestamp ASC;"
    con.execute(sql_request, (track_name, date_trash_left, date_trash_rigth))

    rows = con.fetchall_unbuffered()
    # rows = con.fetchall()

    volume_dict = {}
    time_dict = {}

    for row in rows:
        station = row[1]
        value = row[0]
        date = row[2]
        if station not in volume_dict:
            volume_dict[station] = []
            time_dict[station] = []
        volume_dict[station].append(value)
        time_dict[station].append(date)

    if len(time_dict) == 0:
        return

    fig, ax = plt.subplots()

    for key in volume_dict:
        x = scipy.signal.medfilt(np.array(volume_dict[key]), kernel_size=(3,))
        y = time_dict[key][:len(x)]
        ax.plot(y, x, label=key, marker='.')

    # fig.xlabel('x label')
    # fig.ylabel('y label')

    ax.set_title("%s_%s" % (track_name, track_name))

    ax.legend()
    if not show:
        fig.savefig('./data/track_%s_%s.png' % (track_name, track_name), quality=100, dpi=900)
    else:
        plt.show()

if __name__ == "__main__":
    # trackers = ['A%s' % i for i in range(1, 7)] + ['B%s' % i for i in range(1, 7)] + ['Unknown']
    # for room in [1, 2]:
    #     for tracker in trackers:
    #         get_data(tracker, room)
    # get_data('B2', 1, True)
    get_data_all('B1', True)



