import os
import time
import re
from random import sample
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from pymysql import InternalError, connect
from random import choice

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



if __name__ == "__main__":
    test_fake_bomb()
