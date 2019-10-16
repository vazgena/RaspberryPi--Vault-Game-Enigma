# sudo apt-get install python3-pip
# sudo pip3 install flask
# sudo pip3 install pymysql
# sudo supervisorctl status all


# imports
import os
import re
import time
# import math
from datetime import datetime, timedelta
import logging
import logging.config
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from pymysql import InternalError, connect
from random import choice, sample

import numpy as np
from scipy.optimize import curve_fit

from flask_socketio import SocketIO, emit

logger = logging.getLogger(__name__)

# Variables
app = Flask(__name__)
socketio = SocketIO(app)
dbuser = 'game'
dbpass = 'h95d3T7SXFta'

# Metric number system
# meter_to_feet = 3.281
# A = 0.89976
# B = 9.
# C = 0.111

# number system in foot
meter_to_feet = 1
A = 2.9579865198620396
B = 8.992263513792887
C = 0.35547355086408083

use_rssi = True
# rssi_name = 'rssi'
rssi_name = 'rssi_window'
# use_rssi = False

rssi_buffer = {}


# Basic connection for the database
def data_connect():
    return connect(
        db='game',
        user=dbuser,
        passwd=dbpass,
        host='localhost',
        autocommit=True)


# Redirect to admin_template if no route
@app.route('/')
def entry():
    return redirect(url_for('admin_template'))


# Routing for what game you wish to administer template
@app.route('/adminTemplate')
def admin_template():
    return render_template('adminTempalate.html')


# Allows the user to pick what game they want to administrate and show the status of the game
@app.route('/admin')
def admin():
    vault_is_active = "no"
    connection = data_connect()
    c = connection.cursor()
    check_end = "SELECT * FROM isalive"
    c.execute(check_end)
    row_count = c.rowcount
    if row_count == 0:
        vault_is_active = "Yes"

    connection.close()
    return render_template('admin.html', vault_is_active=vault_is_active)


# On vault this shows all trackes and allows them to be named unnamed trackers are not allowed in the game.
# Aditionally the trackes whould be set to Eddystone-URL with website set to gamine in order for them to be seen.
@app.route('/trackernames', methods=['GET', 'POST'])
def add_id_trackers():
    connection = data_connect()
    c = connection.cursor()
    tracker_list = []
    tracker_list_temp = []
    if request.method == 'POST':
        if request.form['mac']:
            if request.form['mac'] != "Name Not Added Yet":
                mac = request.form['mac']
                name = request.form['name']
                try:
                    insert_tracker_name = "INSERT INTO TrackerNames (mac, name) VALUES (%s, %s) " \
                                          "ON DUPLICATE KEY UPDATE mac = %s, name = %s;"
                    c.execute(insert_tracker_name, (mac, name, mac, name))
                    connection.close()
                    return "Accepted"
                except InternalError:
                    connection.close()
                    return "Failed"
        else:
            connection.close()
            return "Failed"
    else:
        try:
            get_trackers_sql = "SELECT DISTINCT mac FROM trackers"
            c.execute(get_trackers_sql)
            get_trackers = list(c.fetchall())
            for l in get_trackers:
                tracker_list_temp.append(l[0])
                try:

                    get_trackers_name_sql = "SELECT * FROM TrackerNames WHERE mac = %s"
                    c.execute(get_trackers_name_sql, l[0])
                    get_trackers_name = list(c.fetchall())
                    for j in get_trackers_name:
                        name_temp = j[2]
                        if not name_temp:
                            name_temp = "Name Not Added Yet"
                        elif name_temp == "":
                            name_temp = "Name Not Added Yet"

                        tracker_list_temp.append(name_temp)
                except InternalError:
                    tracker_list_temp.append("No Name Added Yet")

                tracker_list.append(tracker_list_temp)
                tracker_list_temp = []
        except InternalError:
            pass

    connection.close()
    return render_template('trackers.html', tracker_list=tracker_list)


# Template for adding tracker names
@app.route('/trackertemplate')
def tracker_template():
    return render_template("trackerstemplate.html")


# Reset uset for game start
# hidden script to start the game if it recieves a POST request it starts the game and truncates all of the tables
# used in game play.
@app.route('/adminStartvault', methods=['GET', 'POST'])
def admin_start_vault():
    connection = data_connect()
    c = connection.cursor()
    if request.method == 'POST':
        # reset all
        # clearList clear
        clear_list_sql = "INSERT INTO clearList (clear) VALUES (%s) ON DUPLICATE KEY UPDATE clear = %s"
        c.execute(clear_list_sql, ("True", "True"))
        # isalive truncate
        bring_alive_update = "TRUNCATE TABLE isalive"
        c.execute(bring_alive_update)
        # ignoreList truncate
        hack_check_update = "TRUNCATE TABLE ignoreList"
        c.execute(hack_check_update)
        # loosing_room truncate
        hack_check_update = "TRUNCATE TABLE loosingTeam"
        c.execute(hack_check_update)
        # hackCheck truncate
        hack_check_update = "TRUNCATE TABLE hackCheck"
        c.execute(hack_check_update)
        # marketOwned truncate
        market_owned_update = "TRUNCATE TABLE marketOwned"
        c.execute(market_owned_update)
        # playerLocation truncate
        reset_trackers = "TRUNCATE TABLE playerLocation"
        c.execute(reset_trackers)
        # trackers truncate
        reset_trackers = "TRUNCATE TABLE trackers"
        c.execute(reset_trackers)
        # bombsDeployed truncate
        bombs_deployed_update = "TRUNCATE TABLE bombsDeployed"
        c.execute(bombs_deployed_update)
        # clear bomb location lists
        market_owned_solo_update = "TRUNCATE TABLE marketbomblocation"
        c.execute(market_owned_solo_update)
        # clear bomb location lists single bomb
        market_owned_solo_update = "TRUNCATE TABLE marketbomblocationsolo"
        c.execute(market_owned_solo_update)
        # audiomanager truncate
        audio_update = "TRUNCATE TABLE audiomanager"
        c.execute(audio_update)
        # defence truncate
        defence_update = "TRUNCATE TABLE station_defence"
        c.execute(defence_update)
        # currency amount 0
        currency_update = "UPDATE currency SET amount = %s WHERE room IS NOT NULL;"
        c.execute(currency_update, "0")
        # hacks howMany 4
        hacks_update = "UPDATE hacks SET howMany = %s WHERE id IS NOT NULL;"
        c.execute(hacks_update, "2")
        # numberOfBombs numberOfBombs 0
        number_of_bombs_update = "UPDATE numberOfBombs SET numberOfBombs = %s WHERE id IS NOT NULL;"
        c.execute(number_of_bombs_update, "0")
        # bomb_detonation_timer_update time 30
        bomb_detonation_timer_update = "UPDATE bombdettimer SET time = %s WHERE id IS NOT NULL;"
        c.execute(bomb_detonation_timer_update, "30")
        log_check = 'UPDATE currency SET amount = %s WHERE room = %s;'
        c.execute(log_check, (request.form['r2Bonus'], "2"))
        log_check = 'UPDATE currency SET amount = %s WHERE room = %s;'
        c.execute(log_check, (request.form['r1Bonus'], "1"))
        trackers_value_update = "TRUNCATE TABLE trackers_value"
        c.execute(trackers_value_update)
        trackers_temp = "TRUNCATE TABLE temp_calibration"
        c.execute(trackers_temp)
        # os.system("python3 resettrackers.py")
    # Close database connection.
    connection.close()
    return redirect(url_for('admin_vault'))


# Reset End


# Admin site for Vault
@app.route('/adminVault')
def admin_vault():
    connection = data_connect()
    c = connection.cursor()
    status_check = 'SELECT * FROM starter  ORDER BY id DESC LIMIT 1'
    c.execute(status_check)
    stat = list(c.fetchall())
    for l in stat:
        if l[2] is None:
            check_end = "SELECT * FROM isalive"
            c.execute(check_end)
            row_count = c.rowcount
            if row_count == 0:
                # Close database connection.
                connection.close()
                return redirect(url_for('game_active_vault'))
            else:
                # Close database connection.
                connection.close()
                return render_template("adminVault.html")
        else:
            # Close database connection.
            connection.close()
            return render_template("adminVault.html")

    # Close database connection.
    connection.close()
    return render_template("adminVault.html")


@app.route('/gameactiveVault')
def game_active_vault():
    sql_volume = "SELECT * from station_volume;"
    connection = data_connect()
    c = connection.cursor()
    c.execute(sql_volume)
    station_volumes = list(c.fetchall())
    volume_level = []
    for station_volume in station_volumes:
        volume_level.append([station_volume[3], station_volume[2]])
    connection.close()
    return render_template('gameactiveVault.html', volume_level=volume_level)


# Shows the trackers locations
@app.route('/playercheckvault', methods=['GET', 'POST'])
def player_check_vault():
    players_location = []
    connection = data_connect()
    c = connection.cursor()
    player_wins = "No one "
    try:
        get_location_sql = "SELECT * FROM playerLocation ORDER BY mac DESC"
        c.execute(get_location_sql)
        get_location = list(c.fetchall())
        for l in get_location:

            do_not_check_sql = "SELECT * FROM bombDetect WHERE mac = %s"
            c.execute(do_not_check_sql, l[1])
            row_count = c.rowcount
            if row_count == 0:
                inner_location = []
                mac_sql_for_conversion = l[1]
                get_name_sql = "SELECT name FROM TrackerNames WHERE mac = %s"
                c.execute(get_name_sql, mac_sql_for_conversion)
                get_name_list = list(c.fetchall())
                for i in get_name_list:
                    mac_sql = i[0]
                location = l[2]
                ble_signal = l[3]
                inner_location.append(mac_sql)
                mac_sql = ""
                room = (location[-1:])
                if room == "1":
                    room_named = "Labyrinth"
                elif room == "2":
                    room_named = "Enigma"
                get_Station_name_sql = "SELECT nameSpelled FROM stationList WHERE name = %s"
                c.execute(get_Station_name_sql, location)
                get_name_spelled_list = list(c.fetchall())
                for i in get_name_spelled_list:
                    location_spelled = i[0]
                inner_location.append(room_named + " " + location_spelled)
                room = ""
                room_named = ""
                location = ""
                location_spelled = ""
                inner_location.append(ble_signal)
                ble_signal = ""
                inner_location.append(mac_sql_for_conversion)
                mac_sql_for_conversion = ""
                players_location.append(inner_location)
                inner_location = []

    except InternalError:
        pass
    try:
        get_looser_sql = "SELECT * FROM loosingTeam"
        c.execute(get_looser_sql)
        winner_list = list(c.fetchall())
        for k in winner_list:
            loosing_room = str(k[1])
            if loosing_room == "1":
                player_wins = "Room 2 "
            if loosing_room == "2":
                player_wins = "Room 1 "
    except InternalError:
        pass
    if request.method == 'POST':
        if request.form['endgame'] == "true":
            game_off_sql = "INSERT INTO isalive (is_alive) VALUES ('no')"
            c.execute(game_off_sql)
    # Close database connection.
    connection.close()
    return render_template('playercheckvault.html', player_wins=player_wins, playersLocation=players_location)


# Game pages

# Listen station template
@app.route('/audiotemplate/<app_id>')
def audio_template(app_id):
    connection = data_connect()
    c = connection.cursor()
    ip_address = ""
    room = app_id
    station = ""
    if room == "1":
        station = "AUD2"
        audio_find = "SELECT * FROM stationlocations WHERE name = %s"
        c.execute(audio_find, station)
        audio_find_sql = list(c.fetchall())
        for i in audio_find_sql:
            ip_address = i[2]
        station = "AUD1"
    if room == "2":
        station = "AUD1"
        audio_find = "SELECT * FROM stationlocations WHERE name = %s"
        c.execute(audio_find, station)
        audio_find_sql = list(c.fetchall())
        for i in audio_find_sql:
            ip_address = i[2]
        station = "AUD2"

    # Close database connection.
    connection.close()
    return render_template('audiotemplate.html', room=room, ipAddress=ip_address,
                           sation=station)


# Listen station data
@app.route('/audioStation/<app_id>')
def audio_station(app_id):
    connection = data_connect()
    c = connection.cursor()
    room = app_id
    if room == '1':
        station = "AUD1"
    elif room == '2':
        station = "AUD2"
    else:
        station = "error"
    message_bomb_20_sec = ""
    message_out = ""
    # Create list of bombs attacking this room if in the air show.
    bmb_check = "SELECT * FROM bombsDeployed WHERE room=%s"
    c.execute(bmb_check, room)
    row_count = c.rowcount
    if row_count != 0:
        get_time_location_list = list(c.fetchall())
        for i in get_time_location_list:
            time_deployed = i[5]
            if time_deployed is None:
                continue
            time_now = datetime.now()
            # Check
            # elapsed_time = time_now - time_deployed
            # if 30 > abs(int(elapsed_time.total_seconds())) > 10:
            #     elapsed_time_reverse = (int(elapsed_time.total_seconds()) - 30) * (-1)
            #     message_bomb_20_sec = "BLAST INCOMING IN {0} SECONDS.".format(str(elapsed_time_reverse))
            # Check
            elapsed_time = time_deployed - time_now
            if 21 > int(elapsed_time.total_seconds()) > -1:
                elapsed_time_reverse = int(elapsed_time.total_seconds())
                message_bomb_20_sec = "BLAST INCOMING IN {0} SECONDS.".format(str(elapsed_time_reverse))

    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    connection.close()

    return render_template('audiostation.html', room=room, station=station,
                           message_bomb_20_sec=message_bomb_20_sec,
                           time_doubler=time_doubler, message_bomb=message_bomb,
                           message_out=message_out)


# Blast station template
@app.route('/bombtemplate/<app_id>')
def bombtemplate(app_id):
    room = app_id
    return render_template('bombtemplate.html', room=room)


# Blast station data
@app.route('/bombStation/<app_id>', methods=['GET', 'POST'])
def bombstation(app_id):
    # DB connection
    connection = data_connect()
    c = connection.cursor()

    # Lists
    stations_deployable = []
    bombs_deployed = []
    names = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []

    # Variables
    currency = 100000
    number_of_bomb_credits = 0
    currencies = 0
    bombs = 0
    added_up = 1
    bombtime = 60
    timetodetonate = 0
    attack_room = ""
    station = ""
    redirect_page_2 = "False"

    # Exchangeable
    room = app_id
    if room == "1":
        station = "BMB1"
        attack_room = "2"
    elif room == "2":
        station = "BMB2"
        attack_room = "1"

    # External functions
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()

    # Check for market item 11 then swap page
    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s;"
    c.execute(check_dual_sql, (room, "11"))
    row_count = c.rowcount
    if row_count != 0:
        # redirect to template 2
        redirect_page_2 = "True"
    else:
        pass

    # Check how many bombs are at this station
    number_of_bombs_sql = 'SELECT * FROM numberOfBombs WHERE room = %s'
    c.execute(number_of_bombs_sql, room)
    number_of_bombs = list(c.fetchall())
    for j in number_of_bombs:
        bombs = j[2]

    # Get list of stations deployable and deployed
    station_list_sql = 'SELECT * FROM stationList WHERE room = %s AND lay_bomb=TRUE;'
    c.execute(station_list_sql, attack_room)
    station_list = list(c.fetchall())
    for i in station_list:
        name = i[1]
        names.append(i[1])
        spelled.append(i[5])
        height_list.append(i[7])
        width_list.append(i[8])
        x_list.append(i[9])
        y_list.append(i[10])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])
        color_selected_list.append(i[15])
        color_list.append(i[16])
        stations_bombed_sql = 'SELECT * FROM bombsDeployed WHERE stationName = %s'
        c.execute(stations_bombed_sql, name)
        row_count = c.rowcount
        if row_count == 0:
            stations_deployable.append(name)
        else:
            added_up = added_up + 1
            bomb_deploy = list(c.fetchall())
            for j in bomb_deploy:
                bombs_deployed.append(j[2])

    # get currency available
    currency_sql = 'SELECT * FROM currency WHERE room=%s'
    c.execute(currency_sql, room)
    currency_get = list(c.fetchall())
    for i in currency_get:
        currencies = i[1]

    # Current cost to deploy a bomb
    bomb_cost = 8
    # bomb_cost = ((int(added_up) * 3) + 3)

    # Post handling
    if request.method == 'POST':

        # Remove the cost of the bomb that is on hold
        if request.form['station'] == "removecost":
            purchaced_bombs_sql = 'SELECT * FROM numberOfBombs WHERE room=%s'
            c.execute(purchaced_bombs_sql, room)
            purchaced_bombs = list(c.fetchall())
            for i in purchaced_bombs:
                number_of_bomb_credits = i[2]
            if number_of_bomb_credits >= 1:
                remove_count = 'UPDATE numberOfBombs SET numberOfBombs = %s WHERE room = %s'
                c.execute(remove_count, ((bombs - 1), room))
            else:
                update_currency = 'UPDATE currency SET amount = %s WHERE room = %s'
                c.execute(update_currency, ((int(currencies) - int(bomb_cost)), room))

        # Start the bomb deploying
        else:
            bomb_insert = 'INSERT INTO bombsDeployed (room, stationName) VALUES (%s, %s)'
            c.execute(bomb_insert, (attack_room, request.form['station']))

            play_add_sql = "INSERT INTO audiomanager (whattoplay, room) VALUES (%s, %s)"
            c.execute(play_add_sql, ("blastlaunch", room))

    timetodetonatebomb = "-1"
    stationsbombedsql = 'SELECT * FROM bombsDeployed WHERE room = %s'
    c.execute(stationsbombedsql, attack_room)
    stationsbombed = list(c.fetchall())
    for j in stationsbombed:
        if j[5]:
            a = j[5]
            b = datetime.now()
            if a > (b - timedelta(seconds=1)):
                timetodetonatebomb = str((a - b).seconds)
                # TODO: hotfix
                if (a - b).seconds > 100:
                    timetodetonatebomb = "0"

    # Close database connection.
    connection.close()

    # render page
    return render_template('bombStation.html', bombtime=bombtime, timeToDetonate=timetodetonate,
                           room=room, names=names, currency=currency,
                           bombCost=bomb_cost, bombs_deployed=bombs_deployed, spelled=spelled,
                           stations_deployable=stations_deployable, bombs=bombs,
                           message_bomb=message_bomb, redirect_page_2=redirect_page_2,
                           time_doubler=time_doubler, width_list=width_list,
                           height_list=height_list, x_list=x_list,
                           y_list=y_list, image_list=image_list, bh_list=bh_list,
                           bw_list=bw_list, br_list=br_list, color_list=color_list,
                           color_selected_list=color_selected_list, station=station,
                           timetodetonatebomb=timetodetonatebomb)


# Blast station change locations template
@app.route('/bombtemplate2/<app_id>')
def bombtemplate2(app_id):
    room = app_id
    return render_template('bombtemplate2.html', room=room)


# Blast station change locations data
@app.route('/bombStation2/<app_id>', methods=['GET', 'POST'])
def bombstation2(app_id):
    connection = data_connect()
    c = connection.cursor()

    # variables
    station = ""
    deploy_now = ""

    bombtime = 60
    timetodetonate = 0
    currency = 100000
    number_of_bomb_credits = 0
    currencies = 0
    bombs = 0
    attack_room = ""
    name_last = ""
    redirect_page_1 = "False"
    room = app_id

    # lists
    bombs_deployed = []
    names = []
    spelled = []
    stations_deployable = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []

    if room == "1":
        station = "BMB1"
        attack_room = "2"

    elif room == "2":
        station = "BMB2"
        attack_room = "1"

    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()

    # redirect to template 1 if they do not own item 11
    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s;"
    c.execute(check_dual_sql, (room, "11"))
    row_count = c.rowcount
    if row_count == 0:
        redirect_page_1 = "True"

    # check how many bombs they have available from the store.
    number_of_bombs_sql = 'SELECT * FROM numberOfBombs WHERE room = %s'
    c.execute(number_of_bombs_sql, room)
    number_of_bombs = list(c.fetchall())
    for j in number_of_bombs:
        bombs = j[2]

    # get list of all rooms and put them in a list
    station_list_sql = 'SELECT * FROM stationList WHERE room = %s AND lay_bomb=TRUE;'
    c.execute(station_list_sql, attack_room)
    station_list = list(c.fetchall())

    # get list of all stations compare them one by one with the temporary locations
    for i in station_list:
        name = i[1]
        names.append(i[1])
        spelled.append(i[5])
        height_list.append(i[7])
        width_list.append(i[8])
        x_list.append(i[9])
        y_list.append(i[10])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])
        color_selected_list.append(i[15])
        color_list.append(i[16])
        stations_bombed_sql = 'SELECT * FROM bombTemp WHERE station = %s'
        c.execute(stations_bombed_sql, name)
        row_count = c.rowcount

        # create temporarily selected and un selected stations and create a list.
        if row_count == 0:
            stations_deployable.append(name)
        else:

            bomb_deploy = list(c.fetchall())

            for j in bomb_deploy:
                bombs_deployed.append(j[2])

    # get number of bombs deployed
    number_of_bombs_deployed_sql = "SELECT * FROM bombsDeployed WHERE room = %s"
    c.execute(number_of_bombs_deployed_sql, attack_room)
    bomb_count = c.rowcount

    # first bomb cost 6 then each after price is increased by 3
    added_up = bomb_count + 1
    bomb_cost = 8
    # bomb_cost = ((int(added_up) * 3) + 3)

    # gather locations of bombs currently deployed.
    get_bomb_temp = "SELECT * FROM bombTemp WHERE room = %s"
    c.execute(get_bomb_temp, attack_room)
    row_count_temp = c.rowcount

    # get currancy
    currency_sql = 'SELECT * FROM currency WHERE room=%s'
    c.execute(currency_sql, room)
    currency_get = list(c.fetchall())
    for i in currency_get:
        currencies = i[1]

    # if the number of bombs exceeds the number of bombs then start activation of the bombs.
    if request.method != 'POST':
        if (added_up - 1) < row_count_temp:
            # check for run once
            run_once_check = "SELECT * FROM bomb2RunOnce WHERE station = %s "
            c.execute(run_once_check, room)
            row_count_runonce = c.rowcount
            if row_count_runonce == 0:
                deploy_now = "yes"
                # print("runonce")
                insert_run_once = "INSERT INTO bomb2RunOnce (station, runeOnce) VALUES (%s, %s)"
                c.execute(insert_run_once, (room, "1"))

                # Bill players for bombs deployed
                purchased_bombs_sql = 'SELECT * FROM numberOfBombs WHERE room = %s'
                c.execute(purchased_bombs_sql, room)
                purchased_bombs = list(c.fetchall())
                for i in purchased_bombs:
                    number_of_bomb_credits = i[2]
                if number_of_bomb_credits >= 1:
                    remove_count = 'UPDATE numberOfBombs SET numberOfBombs = %s WHERE room = %s'
                    c.execute(remove_count, ((bombs - 1), room))
                else:
                    update_currency = 'UPDATE currency SET amount = %s WHERE room = %s'
                    c.execute(update_currency, ((int(currencies) - int(bomb_cost)), room))

    # posting of data from page
    if request.method == 'POST':
        station_form = request.form['station']

        # make activation run only once
        if station_form == "messageSent":
            deploy_now = "no"
            # print("runonce ended")
            insert_run_once = "INSERT INTO bomb2RunOnce (station, runeOnce) VALUES (%s, %s)"
            c.execute(insert_run_once, (room, "1"))

        # check to see if bomb has been added to temp and switch it off if it is on
        elif station_form not in stations_deployable:
            delete_station_sql = "DELETE FROM bombTemp WHERE station = %s"
            c.execute(delete_station_sql, station_form)
            # added clear in case of issues found in alpha testing.
            run_once_check = "DELETE FROM bomb2RunOnce WHERE station = %s"
            c.execute(run_once_check, room)

        # check to see if bomb has not been added to temp and switch it on if off
        elif station_form in stations_deployable:
            bomb_insert_temp = 'INSERT INTO bombTemp (room, station) VALUES (%s, %s)'
            c.execute(bomb_insert_temp, (attack_room, station_form))
            # added clear in case of issues found in alpha testing.
            run_once_check = "DELETE FROM bomb2RunOnce WHERE station = %s"
            c.execute(run_once_check, room)

        # if bomb needs to be deployed then deploy all bombs in play again and turn off activation sequence.
        if station_form == "deploynow":
            run_once_check = "DELETE FROM bomb2RunOnce WHERE station = %s"
            c.execute(run_once_check, room)
            insert_run_once = "INSERT INTO bomb2RunOnce (station, runeOnce) VALUES (%s, %s)"
            c.execute(insert_run_once, (room, "2"))
            # get the list from the bombTemp table
            select_station_sql = "SELECT * FROM bombTemp WHERE room = %s"
            c.execute(select_station_sql, attack_room)
            selected_station_list = list(c.fetchall())
            bomb_clear = "DELETE FROM bombsDeployed WHERE room = %s"
            c.execute(bomb_clear, attack_room)
            ignore_clear = "DELETE FROM ignoreList WHERE room = %s"
            c.execute(ignore_clear, attack_room)
            for i in selected_station_list:
                bomb_insert = 'INSERT INTO ignoreList (room, station) VALUES (%s, %s)'
                c.execute(bomb_insert, (attack_room, i[1]))
                # insert into bombs deployed with date that exceeds all timers
                bomb_insert = 'INSERT INTO bombsDeployed (room, stationName, timeDeployed) VALUES (%s, %s, %s)'
                c.execute(bomb_insert, (attack_room, i[1], "2000-01-01 00:00:01"))

                # storing varible that will hold the last bomb laid
                name_last = i[1]

            # set the time to now to activate bomb launches.
            bomb_insert = 'DELETE FROM bombsDeployed WHERE stationName = %s'
            c.execute(bomb_insert, name_last)
            bomb_insert = 'INSERT INTO bombsDeployed (room, stationName) VALUES (%s, %s)'
            c.execute(bomb_insert, (attack_room, name_last))
            ignore_clear2 = "DELETE FROM ignoreList WHERE station = %s"
            c.execute(ignore_clear2, name_last)

    # Check to see if room has lost won or is in play
    get_looser_sql = "SELECT * FROM loosingTeam"
    c.execute(get_looser_sql)
    row_count = c.rowcount
    if row_count != 0:
        winner_list = list(c.fetchall())
        for k in winner_list:
            loosing_room = str(k[1])
            if loosing_room != room:
                message_bomb = "YOU WIN"
            else:
                if k[3] == "BMB1" or "BMB2":
                    message_bomb = "YOU LOSE - BOMB DETONATED HERE"
                else:
                    message_bomb = "YOU LOSE"

    # Close database connection.
    connection.close()
    return render_template('bombStation2.html', bombtime=bombtime, timeToDetonate=timetodetonate,
                           time_doubler=time_doubler, room=room, names=names, currency=currency,
                           bombCost=bomb_cost, bombs_deployed=bombs_deployed, spelled=spelled,
                           stations_deployable=stations_deployable, bombs=bombs, message_bomb=message_bomb,
                           deploy_now=deploy_now, redirect_page_1=redirect_page_1,
                           width_list=width_list, height_list=height_list, x_list=x_list,
                           y_list=y_list, image_list=image_list, bh_list=bh_list,
                           bw_list=bw_list, br_list=br_list, color_list=color_list,
                           color_selected_list=color_selected_list, station=station)


# Watch station template
@app.route('/cameraTemplate/<app_id>/<room>', methods=['GET', 'POST'])
def camera_template(app_id, room):
    connection = data_connect()
    c = connection.cursor()
    station = app_id
    cam_list = []
    atkroom = ""
    if room == "1":
        atkroom = "2"
    if room == "2":
        atkroom = "1"
    camera_locations_sql = "SELECT * FROM cameraLocations WHERE room = %s;"
    c.execute(camera_locations_sql, atkroom)
    cam_listed = list(c.fetchall())
    for i in cam_listed:
        cam_list.append(i[1])
    else:
        cams_available = "1"

    # Close database connection.
    connection.close()
    return render_template('cameraTemplate.html', room=room, cam_list=cam_list, station=station,
                           cams_available=cams_available)


# Watch station data
@app.route('/cameraStation/<app_id>/<room>', methods=['GET', 'POST'])
def camera_station(app_id, room):
    connection = data_connect()
    c = connection.cursor()
    station = app_id
    atkroom = "0"
    timer_message = ""

    if room == "1":
        atkroom = "2"
    if room == "2":
        atkroom = "1"

    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s;"
    c.execute(check_dual_sql, (room, "6"))
    row_count = c.rowcount

    if row_count != 0:
        cams_available = "2"
    else:
        cams_available = "1"

    get_quantity_available = "SELECT * FROM marketOwned WHERE itemID = %s AND " \
                             "team=%s AND time_bought BETWEEN NOW() -" \
                             "INTERVAL 5 MINUTE AND NOW()"
    c.execute(get_quantity_available, ("8", atkroom))
    counted_market = c.rowcount
    if counted_market != 0:
        cams_available = "0"
        rows_bloks = list(c.fetchall())
        time_bloks = max([row[7] for row in rows_bloks])
        time_now = datetime.now()
        time_left_sec = 300 - int((time_now - time_bloks).total_seconds())
        timer_message = "YOUR CAMERAS HAVE BEEN SHUT DOWN. {0}:{1:02d} UNTIL THEY ARE BACK ONLINE." \
            .format(time_left_sec // 60, time_left_sec % 60)
    # Close database connection.
    connection.close()
    return render_template('cameraStation.html', cams_available=cams_available,
                           time_doubler=time_doubler, message_bomb=message_bomb, station=station,
                           timer_message=timer_message)


# # Test code
# # Watch station data
# time_start = datetime.now()
# @app.route('/cameraStation/<app_id>/<room>', methods=['GET', 'POST'])
# def camera_station(app_id, room):
#     try:
#         station = app_id
#         atkroom = "0"
#         timer_message = ""
#
#         if room == "1":
#             atkroom = "2"
#         if room == "2":
#             atkroom = "1"
#
#         time_doubler = time_doubler_check(station)
#         message_bomb = looser_check()
#
#
#         cams_available = "0"
#         global time_start
#         rows_bloks = [[time_start, ]*8 for i in range(2)]
#         time_bloks = max([row[7] for row in rows_bloks])
#         time_now = datetime.now()
#         time_left_sec = 300 - int((time_now - time_bloks).total_seconds())
#         timer_message = "YOUR CAMERAS HAVE BEEN SHUT DOWN. {0}:{1} UNTIL THEY ARE BACK ONLINE." \
#             .format(time_left_sec//60, time_left_sec%60)
#         # Close database connection.
#     except:
#         a = 1
#
#     # TODO: added timer check and add value for render_template, timer from counted_market
#     return render_template('cameraStation.html', cams_available=cams_available,
#                            time_doubler=time_doubler, message_bomb=message_bomb, station=station,
#                            timer_message=timer_message)


# Hack station template
@app.route('/hacktemplate/<app_id>')
def hack_template(app_id):
    room = app_id
    response = render_template('hacktemplate.html', room=room)
    return response


# Hack station data
@app.route('/hackStation/<app_id>', methods=['GET', 'POST'])
def hack_station(app_id):
    connection = data_connect()
    c = connection.cursor()
    room = app_id
    currencies = "0"
    station = ""
    if room == "1":
        station = "HAC1"
    elif room == "2":
        station = "HAC2"
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    attack_room = "0"
    station_listed = []
    rooms_available = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []
    if room == "1":
        attack_room = "2"
    elif room == "2":
        attack_room = "1"
    how_much_time = 60
    how_many_hacks = 0
    hack_count_check = 'SELECT * FROM hacks WHERE team = %s'
    c.execute(hack_count_check, str(room))
    hack_count_sql = list(c.fetchall())

    for i in hack_count_sql:
        how_many_hacks = i[2]

    if request.method == 'POST':
        hack_stations = 'INSERT INTO hackCheck (roomstation, status, timeRemaining) VALUES (%s, %s, %s)'
        c.execute(hack_stations, (request.form['station'], "hacked", how_much_time))
        funding1 = "INSERT INTO hacks (team, howMany) VALUES (%s, %s) ON DUPLICATE KEY UPDATE team = %s, howMany = %s;"
        c.execute(funding1, (room, int(how_many_hacks) - 1, room, int(how_many_hacks) - 1))
        add_coin_available = "SELECT * FROM marketOwned WHERE itemID = %s AND team=%s AND station = %s"
        c.execute(add_coin_available, ("15", attack_room, request.form['station']))
        counted_coin = c.rowcount
        if counted_coin != 0:
            currency_sql = 'SELECT * FROM currency WHERE room=%s'
            c.execute(currency_sql, attack_room)
            currency_get = list(c.fetchall())
            for i in currency_get:
                currencies = i[1]
            update_currency = 'UPDATE currency SET amount = %s WHERE room = %s'
            c.execute(update_currency, ((int(currencies) + 1), attack_room))
        else:
            pass

    station_list = "SELECT * FROM stationList WHERE room = %s"
    c.execute(station_list, attack_room)
    station_list_sql = list(c.fetchall())
    for i in station_list_sql:
        spelled.append(i[5])
        room_hack_check = 'SELECT * FROM hackCheck WHERE roomstation = %s'
        c.execute(room_hack_check, i[1])
        row_count = c.rowcount
        if row_count == 0:
            rooms_available.append(i[1])

        # name = 1 room = 2 nameSpelled = 5
        # height = 7 width = 8 x = 9 y = 10 image = 11

        station_listed.append(i[1])
        height_list.append(i[7])
        width_list.append(i[8])
        x_list.append(i[19])
        y_list.append(i[20])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])
        color_selected_list.append(i[15])
        color_list.append(i[16])

    get_quantity_available = "SELECT * FROM marketOwned WHERE itemID = %s AND team=%s"
    c.execute(get_quantity_available, ("22", room))
    counted_market = c.rowcount
    if counted_market != 0:
        check_sec = "yes"
    else:
        check_sec = "no"

    # Close database connection.
    connection.close()
    return render_template('hackStation.html', stationListed=station_listed, room=room,
                           howManyHacks=how_many_hacks, spelled=spelled,
                           message_bomb=message_bomb, roomsAvailable=rooms_available,
                           time_doubler=time_doubler, check_sec=check_sec,
                           width_list=width_list, height_list=height_list, x_list=x_list,
                           y_list=y_list, image_list=image_list, bh_list=bh_list,
                           bw_list=bw_list, br_list=br_list, color_list=color_list,
                           color_selected_list=color_selected_list, station=station)


# Mirror station template
@app.route('/maintemplate_old/<app_id>')
def maintemplate(app_id):
    room = app_id

    return render_template('maintemplate.html', room=room)


# Mirror station data
@app.route('/mainstation_old/<app_id>')
def mainstation(app_id):
    connection = data_connect()
    c = connection.cursor()
    room = app_id
    station_listed = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []
    station = ""
    if room == "1":
        station = "MAN1"
    elif room == "2":
        station = "MAN2"
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    station_list = "SELECT * FROM stationList WHERE room = %s"
    c.execute(station_list, room)
    station_list_sql = list(c.fetchall())
    for i in station_list_sql:
        if i[1] != "MAN1" and i[1] != "AUD1" and i[1] != "MAN2" and i[1] != "AUD2" \
                and i[1] != "CS21" and i[1] != "CS22":
            station_listed.append(i[1])
            spelled.append(i[5])
            height_list.append(i[7])
            width_list.append(i[8])
            x_list.append(i[17])
            y_list.append(i[18])
            image_list.append(i[11])
            bh_list.append(i[12])
            bw_list.append(i[13])
            br_list.append(i[14])
            color_selected_list.append(i[15])
            color_list.append(i[16])
    connection.close()
    return render_template('mainstation.html', room=room, spelled=spelled,
                           message_bomb=message_bomb, stationListed=station_listed,
                           time_doubler=time_doubler, width_list=width_list,
                           height_list=height_list, x_list=x_list,
                           y_list=y_list, image_list=image_list, bh_list=bh_list,
                           bw_list=bw_list, br_list=br_list, color_list=color_list,
                           color_selected_list=color_selected_list, station=station)


# Market station template
@app.route('/markettemplate/<app_id>')
def markettemplate(app_id):
    room = app_id
    return render_template('markettemplate.html', room=room)


# Market station data
@app.route('/marketstation/<app_id>', methods=['GET', 'POST'])
def market(app_id):
    connection = data_connect()
    c = connection.cursor()
    currency2 = 0
    marketapplett = []
    room = app_id
    station = ""
    if room == "1":
        station = "MKP1"
    elif room == "2":
        station = "MKP2"
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    number_owned_total = 0
    number_owned = 0
    discount = 0
    hacks = 0
    bombs = 0
    atkroom = ""
    coin = 0
    market_owned_listed = []
    market_owned_temp = []
    market_selectable = ""
    bomb_location_text_output = "nothing"
    bomb_location_text_output_only_1 = "nothing"
    # Get list of available purchases
    marketsql = "SELECT * FROM marketCurrent WHERE purchased = %s"
    c.execute(marketsql, "No")
    marketlist = list(c.fetchall())
    try:
        get_discount_available_sql = "SELECT * FROM marketOwned WHERE team = %s AND activated = %s"
        c.execute(get_discount_available_sql, (room, "yes"))
        check_discount_sql = list(c.fetchall())
        for m in check_discount_sql:
            if m[4] == 27:
                discount = discount + 1
    except InternalError:
        pass
    for i in marketlist:
        # See if purchasable due to quantity limitations.
        get_quantity_available = "SELECT * FROM marketOwned WHERE itemID = %s"
        c.execute(get_quantity_available, i[0])
        counted = c.rowcount

        market_id = i[5]
        market_text = i[1]
        market_cost = i[2] - discount
        market_multiple_allowed = i[3]

        get_market_selectable = "SELECT * FROM market WHERE id = %s"
        c.execute(get_market_selectable, market_id)
        market_selector_list = list(c.fetchall())
        for k in market_selector_list:
            market_selectable = k[4]

        updated_market_list = [market_id, market_text, str(market_cost), market_multiple_allowed, market_selectable]
        if counted == 0:
            marketapplett.append(updated_market_list)
        else:
            check_quantity_owned = list(c.fetchall())
            for j in check_quantity_owned:
                number_owned_total = number_owned_total + int(j[2])
            if number_owned_total < int(i[3]):
                marketapplett.append(updated_market_list)
    market_owned_sql = "SELECT * FROM marketOwned WHERE team = %s AND activated = %s"
    c.execute(market_owned_sql, (room, "yes"))
    market_owned_list = list(c.fetchall())

    for i in market_owned_list:
        market_owned_temp.append(i[1])
        market_owned_temp.append(i[4])
        market_owned_listed.append(market_owned_temp)
        market_owned_temp = []

        if i[4] == 12:
            get_locations_output_sql = "SELECT * FROM marketbomblocation WHERE room = %s"
            c.execute(get_locations_output_sql, room)
            location_list = list(c.fetchall())
            for j in location_list:
                bomb_location_text_output = j[1]

        elif i[4] == 25:
            get_locations_output_sql = "SELECT * FROM marketbomblocationsolo WHERE room = %s"
            c.execute(get_locations_output_sql, room)
            location_list = list(c.fetchall())
            for j in location_list:
                bomb_location_text_output_only_1 = j[1]

    # Submit purchases
    if request.method == 'POST':
        if room == "1":
            atkroom = "2"
        elif room == "2":
            atkroom = "1"

        if "station" in request.form:
            station_form = request.form['station']
            station_insert = "UPDATE marketOwned SET station=%s WHERE itemID=%s"
            c.execute(station_insert, (station_form, request.form['itemID']))
            return "sent"

        if request.form['activated'] == "no":
            display_text = ""
            # Check how much currency the person has.
            getcurrencysql = "SELECT * FROM currency WHERE room = %s"
            c.execute(getcurrencysql, room)
            getcurrencylist = list(c.fetchall())
            for i in getcurrencylist:
                currency2 = i[1]
            # Check stats of item.
            get_quantity_available = "SELECT * FROM marketOwned WHERE itemID = %s AND team=%s"
            c.execute(get_quantity_available, (request.form['itemID'], room))
            counted2 = c.rowcount

            if counted2 == 0:
                marketsql = "SELECT * FROM marketCurrent WHERE itemID = %s"
                c.execute(marketsql, request.form['itemID'])
                marketlist = list(c.fetchall())
                for i in marketlist:
                    display_text = i[1]
                insert_market = "INSERT INTO marketOwned (itemID, text, numberOwned, team) VALUES (%s, %s, %s, %s);"
                c.execute(insert_market, (request.form['itemID'], display_text, "1", room))
            else:
                number_owned_list = list(c.fetchall())
                for k in number_owned_list:
                    number_owned = k[2]
                insert_market = "UPDATE marketOwned SET numberOwned=%s WHERE itemID=%s AND team=%s;"
                c.execute(insert_market, (int(number_owned) + 1, request.form['itemID'], room))
            # Remove item from the marketplace
            update_available_now = 'UPDATE marketCurrent SET purchased = %s WHERE itemID=%s;'
            c.execute(update_available_now, ("Yes", request.form['itemID']))

            # Update currency
            currency2 = (int(currency2) - int(request.form['cost']))
            update_currency_sql = "UPDATE currency SET amount = %s WHERE room = %s;"
            c.execute(update_currency_sql, (currency2, room))
        elif request.form['activated'] == "yes":
            activate_market = "UPDATE marketOwned SET activated=%s WHERE itemID=%s AND team=%s;"
            c.execute(activate_market, ("yes", request.form['itemID'], room))

            # see the location of all bombs
            if str(request.form['itemID']) == "12":
                bomb_location_text = "You found bombs located at "
                get_locations_of_bombs_sql = "SELECT * FROM bombsDeployed WHERE room = %s AND fake_bomb=FALSE ;"
                c.execute(get_locations_of_bombs_sql, room)
                row_count_bombs = c.rowcount
                if row_count_bombs != 0:
                    get_locations_of_bombs_list = list(c.fetchall())
                    for i in get_locations_of_bombs_list:
                        get_text_sql = "SELECT * FROM stationList WHERE name = %s"
                        c.execute(get_text_sql, i[2])
                        get_text_list = list(c.fetchall())
                        for j in get_text_list:
                            bomb_location_text = bomb_location_text + ", " + j[5]
                else:
                    bomb_location_text = "Your opponent has not deployed any bombs"
                add_location_text_sql = 'INSERT INTO marketbomblocation (locations, room) VALUES (%s, %s)'
                c.execute(add_location_text_sql, (bomb_location_text, room))

            # see the location of one bomb
            if str(request.form['itemID']) == "25":
                bomb_location_text = "You found a bomb located at "
                get_locations_of_bombs_sql = "SELECT * FROM bombsDeployed WHERE room = %s AND fake_bomb=FALSE ORDER BY RAND() LIMIT 1"
                c.execute(get_locations_of_bombs_sql, room)
                row_count_bombs = c.rowcount
                if row_count_bombs != 0:
                    get_locations_of_bombs_list = list(c.fetchall())
                    for i in get_locations_of_bombs_list:
                        get_text_sql = "SELECT * FROM stationList WHERE name = %s"
                        c.execute(get_text_sql, i[2])
                        get_text_list = list(c.fetchall())
                        for j in get_text_list:
                            bomb_location_text = bomb_location_text + ", " + j[5]
                else:
                    bomb_location_text = "Your opponent has not deployed any bombs"
                add_location_text_sql = 'INSERT INTO marketbomblocationsolo (locations, room) VALUES (%s, %s)'
                c.execute(add_location_text_sql, (bomb_location_text, room))

            if str(request.form['itemID']) == "9":
                hack_checker_sql = "SELECT * FROM hacks WHERE team = %s"
                c.execute(hack_checker_sql, room)
                hack_check_list = list(c.fetchall())
                for l in hack_check_list:
                    hacks = int(l[2])
                hacks_added = int(hacks) + 4
                update_currency_sql = 'UPDATE hacks SET howmany = %s WHERE team = %s;'
                c.execute(update_currency_sql, (str(hacks_added), room))

            elif str(request.form['itemID']) == "13":
                station_remove = "DELETE FROM ignoreList WHERE room = %s LIMIT 1"
                c.execute(station_remove, atkroom)
                ten_sec = "INSERT INTO `10secdrop` (room) VALUES (%s);"
                c.execute(ten_sec, atkroom)

            elif str(request.form['itemID']) == "10":
                hack_checker_sql = "SELECT * FROM hacks WHERE team = %s"
                c.execute(hack_checker_sql, room)
                hack_check_list = list(c.fetchall())
                for l in hack_check_list:
                    hacks = int(l[2])
                hacks_added = int(hacks) + 6
                update_currency_sql = 'UPDATE hacks SET howmany = %s WHERE team = %s;'
                c.execute(update_currency_sql, (str(hacks_added), room))

            elif str(request.form['itemID']) == "16":
                checker_sql = "SELECT * FROM numberOfBombs WHERE room = %s"
                c.execute(checker_sql, room)
                check_list = list(c.fetchall())
                for l in check_list:
                    bombs = int(l[2])
                bombs_added = int(bombs) + 1
                update_currency_sql = 'UPDATE numberOfBombs SET numberOfBombs = %s WHERE room = %s;'
                c.execute(update_currency_sql, (str(bombs_added), room))

            elif str(request.form['itemID']) == "28":
                checker_sql = "SELECT * FROM currency WHERE room = %s"
                c.execute(checker_sql, room)
                check_list = list(c.fetchall())
                for l in check_list:
                    coin = int(l[1])
                coin_added = int(coin) + 15
                update_currency_sql = 'UPDATE currency SET amount = %s WHERE room = %s;'
                c.execute(update_currency_sql, (str(coin_added), room))

            elif str(request.form['itemID']) == "24":
                # TODO: modify
                if str(room) == "1":
                    atkroom = "2"
                if str(room) == "2":
                    atkroom = "1"
                station_names = []
                room_list_sql = "SELECT * FROM stationList WHERE room = %s AND lay_bomb=TRUE;"
                c.execute(room_list_sql, atkroom)
                room_list = list(c.fetchall())
                for w in room_list:
                    station_names.append(w[1])
                bomb_check = "SELECT * FROM bombsDeployed WHERE room = %s"
                c.execute(bomb_check, atkroom)
                bomb_list = list(c.fetchall())
                existing_bombs = [b[2] for b in bomb_list]
                new_bombs = []

                for g in bomb_list:
                    station_name = choice(station_names)
                    station_names.remove(station_name)
                    bomb_id = g[0]
                    bomb_update = "UPDATE bombsDeployed SET stationName = %s WHERE id = %s;"
                    c.execute(bomb_update, (station_name, bomb_id))
                    ignoreList_update = "UPDATE ignoreList SET station = %s WHERE station = %s;"
                    c.execute(ignoreList_update, (station_name, g[2]))
                    new_bombs.append(station_name)

                # for station in set(new_bombs).difference(set(existing_bombs)):
                #     bomb_ignore_remove = "DELETE FROM ignoreList WHERE station=%s;"
                #     c.execute(bomb_ignore_remove, station)

            elif str(request.form['itemID']) == "21":
                current_ttd_sql = "SELECT * FROM bombdettimer WHERE room = %s"
                c.execute(current_ttd_sql, atkroom)
                current_ttd_list = list(c.fetchall())
                for x in current_ttd_list:
                    current_ttd_mod = str(int(x[2]) - 10)
                    current_ttd_update = "UPDATE bombdettimer SET time = %s WHERE room = %s"
                    c.execute(current_ttd_update, (current_ttd_mod, atkroom))

            elif str(request.form['itemID']) == "29":
                if str(room) == "1":
                    atkroom = "2"
                if str(room) == "2":
                    atkroom = "1"
                sql_query = "INSERT INTO bombsDeployed (room, fake_bomb, stationName, timeDeployed) VALUES (%s,TRUE, %s, %s);"
                c.execute(sql_query, (atkroom, '', datetime.now()))

            elif str(request.form['itemID']) == "30":
                # Random hacking 3 stations
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
                else:
                    stations_hack = sample(room_list, 3)
                for station in stations_hack:
                    station_name = station[1]
                    hack_stations = 'INSERT INTO hackCheck (roomstation, status, timeRemaining) VALUES (%s, %s, %s)'
                    c.execute(hack_stations, (station_name, "hacked", how_much_time))
                    funding1 = "INSERT INTO hacks (team, howMany) VALUES (%s, %s) ON DUPLICATE KEY UPDATE team = %s, howMany = %s;"
                    c.execute(funding1, (room, int(how_many_hacks) - 1, room, int(how_many_hacks) - 1))
                    how_many_hacks -= 1

    for row in marketapplett:
        row.append(re.sub(r"(?<!\\)'", "\\'", row[1]))
        # unlock flag
        row.append('true')

    # Lock on current blast
    id_markets = set([int(row[0]) for row in marketapplett])
    set_locked_bomb = set([13, 24, 29])
    if id_markets.intersection(set_locked_bomb):
        if str(room) == "1":
            atkroom = "2"
        if str(room) == "2":
            atkroom = "1"
        sql_query = "SELECT bombsDeployed.* FROM bombsDeployed LEFT JOIN ignoreList ON bombsDeployed.stationName=ignoreList.station" \
                    " WHERE bombsDeployed.room=%s AND ignoreList.room IS NULL AND bombsDeployed.fake_bomb=FALSE;"
        c.execute(sql_query, atkroom)
        row_count = c.rowcount
        if row_count > 0:
            for row in marketapplett:
                if int(row[0]) in set_locked_bomb:
                    # lock flag
                    row[6] = 'false'

    # Close database connection.
    connection.close()
    return render_template('marketstation.html', market_owned_listed=market_owned_listed,
                           marketApplett=marketapplett, room=room,
                           time_doubler=time_doubler, message_bomb=message_bomb,
                           bomb_location_text_output_only_1=bomb_location_text_output_only_1,
                           bomb_location_text_output=bomb_location_text_output, station=station)


# Market station selector is used if a station needs to be selected for a market purchase
@app.route('/marketselector/<app_id>')
def marketselector(app_id):
    connection = data_connect()
    c = connection.cursor()
    room = app_id
    names = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []
    station_list_sql = 'SELECT * FROM stationList WHERE room = %s;'
    c.execute(station_list_sql, room)
    station_list = list(c.fetchall())
    for i in station_list:
        name = i[1]
        names.append(name)
        spelled.append(i[5])
        height_list.append(i[7])
        width_list.append(i[8])
        x_list.append(i[21])
        y_list.append(i[22])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])
        color_selected_list.append(i[15])
        color_list.append(i[16])
    connection.close()
    return render_template('marketselector.html', names=names,
                           spelled=spelled, color_list=color_list, x_list=x_list,
                           y_list=y_list, image_list=image_list, bh_list=bh_list,
                           bw_list=bw_list, br_list=br_list, color_selected_list=color_selected_list,
                           width_list=width_list, height_list=height_list)


# Assist station template
@app.route('/mastertemplate/<app_id>')
def mastertemplate(app_id):
    room = app_id
    return render_template('mastertemplate.html', room=room)


# Assist station data
@app.route('/masterStation/<app_id>', methods=['GET', 'POST'])
def masterstation(app_id):
    connection = data_connect()
    c = connection.cursor()
    room = app_id
    station = ""
    if room == "1":
        station = "MAS1"
    elif room == "2":
        station = "MAS2"
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    station_listed = []
    doubler_station = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []

    doubler_station_active = ""
    check_doubler_sql = "SELECT * FROM timeDoubler WHERE room = %s"
    c.execute(check_doubler_sql, room)
    check_doubler_list_sql = list(c.fetchall())
    for j in check_doubler_list_sql:
        doubler_station.append(j[1])
    station_list = 'SELECT * FROM stationList WHERE room = %s'
    c.execute(station_list, room)
    station_list_sql = list(c.fetchall())
    for i in station_list_sql:
        spelled.append(i[5])
        height_list.append(i[7])
        width_list.append(i[8])
        x_list.append(i[17])
        y_list.append(i[18])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])
        if len(i) < 24:
            # hot fix, can be deleted after making changes to the database
            color_selected_list.append('#880000; border-style: none; background: transparent !important; border:0 '
                                       '!important; filter: brightness(.50) hue-rotate(150deg)  saturate(5) !important;')
        else:
            color_selected_list.append(i[23])
        color_list.append(i[16])
        if i[1] in doubler_station:
            doubler_station_active = i[1]
            station_listed.append(i[1])
        else:
            station_listed.append(i[1])

    if request.method == 'POST':
        is_time_double_active_sql = "SELECT * FROM timeDoubler WHERE room = %s"
        c.execute(is_time_double_active_sql, room)
        row_count = c.rowcount
        if row_count != 0:
            station_remove = "DELETE FROM timeDoubler WHERE room = %s"
            c.execute(station_remove, room)
        station_insert_sql = "INSERT INTO timeDoubler (station, doubler, room) VALUES (%s, %s, %s)"
        c.execute(station_insert_sql, (request.form['station'], "double", room))

    # Close database connection.
    connection.close()
    return render_template('masterStation.html', room=room, spelled=spelled,
                           stationListed=station_listed, time_doubler=time_doubler,
                           doublerStationActive=doubler_station_active,
                           message_bomb=message_bomb,
                           width_list=width_list, height_list=height_list, x_list=x_list,
                           y_list=y_list, image_list=image_list, bh_list=bh_list,
                           bw_list=bw_list, br_list=br_list, color_list=color_list,
                           color_selected_list=color_selected_list, station=station)


# Harvest station data
@app.route('/minethis/<app_id>', methods=['GET', 'POST'])
def mine_this(app_id):
    connection = data_connect()
    c = connection.cursor()
    room = app_id
    names = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []
    this_room_collected = "no"
    collected_mine = "no"
    color = "none"
    station = ""
    currency = 0
    is_available = "Yes"
    if room == "1":
        station = "MTR1"
    if room == "2":
        station = "MTR2"
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    if request.method == 'POST':
        station_check = request.form['station']
        check_station_sql = "SELECT * FROM currentColor WHERE station = %s"
        c.execute(check_station_sql, station_check)
        row_count = c.rowcount
        if row_count != 0:
            update_mine_sql = "UPDATE currentColor SET roomCollected = %s, collected = %s WHERE station = %s"
            c.execute(update_mine_sql, (room, "Yes", station_check))
            get_cur_to_add_sql = "SELECT * FROM currency WHERE room = %s"
            c.execute(get_cur_to_add_sql, room)
            get_cur_to_add = list(c.fetchall())
            for i in get_cur_to_add:
                check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s"
                c.execute(check_dual_sql, (room, "1"))
                row_count = c.rowcount
                if row_count != 0:
                    currency = int(i[1]) + 2
                else:
                    currency = int(i[1]) + 1
                if color == "green":
                    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s"
                    c.execute(check_dual_sql, (room, "3"))
                    row_count = c.rowcount
                    if row_count != 0:
                        currency = currency + 2
                if color == "red":
                    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s"
                    c.execute(check_dual_sql, (room, "4"))
                    row_count = c.rowcount
                    if row_count != 0:
                        currency = currency + 2
                if color == "yellow":
                    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s"
                    c.execute(check_dual_sql, (room, "5"))
                    row_count = c.rowcount
                    if row_count != 0:
                        currency = currency + 2
            add_cur_sql = "UPDATE currency SET amount = %s WHERE room = %s;"
            c.execute(add_cur_sql, (currency, room))

            play_add_sql = "INSERT INTO audiomanager (whattoplay, room) VALUES (%s, %s)"
            c.execute(play_add_sql, ("charge", room))
        else:
            insert_lock = "INSERT INTO mineLockOut (station) VALUES (%s);"
            c.execute(insert_lock, station)

    mine_collected_sql = "SELECT * FROM currentColor WHERE room = %s AND collected = %s"
    c.execute(mine_collected_sql, (room, "Yes"))
    row_count_mined = c.rowcount
    if row_count_mined != 0:
        collected_mine = "yes"
        mine_collected_room_sql = "SELECT * FROM currentColor WHERE roomCollected = %s AND room = %s"
        c.execute(mine_collected_room_sql, (room, room))
        row_count_mined_room = c.rowcount
        if row_count_mined_room != 0:
            this_room_collected = "yes"
        else:
            this_room_collected = "no"

    check_lockout_sql = "SELECT * FROM  mineLockOut WHERE station = %s;"
    c.execute(check_lockout_sql, station)

    row_count = c.rowcount
    if row_count != 0:
        station_check_list = list(c.fetchall())
        for j in station_check_list:
            time_to_unlock = j[2]
            time_now = datetime.now()
            elapsed_time = time_now - time_to_unlock
            if elapsed_time.total_seconds() > 30:
                remove_lockout = "DELETE FROM mineLockOut WHERE station = %s"
                c.execute(remove_lockout, station)
            else:
                is_available = "Yes"
                connection.close()
                return render_template('minethis.html', color=color, time_doubler=time_doubler,
                                       is_available=is_available, collected_mine=collected_mine,
                                       stationListed=names, spelled=spelled, station=station,
                                       room=room, message_bomb=message_bomb,
                                       this_room_collected=this_room_collected,
                                       width_list=width_list, height_list=height_list, x_list=x_list,
                                       y_list=y_list, image_list=image_list, bh_list=bh_list,
                                       bw_list=bw_list, br_list=br_list, color_list=color_list,
                                       color_selected_list=color_selected_list)

    # station_list_sql = 'SELECT * FROM stationList WHERE room = %s;'
    station_list_sql = 'SELECT * FROM stationList WHERE room = %s AND is_visible = TRUE;'
    c.execute(station_list_sql, room)
    station_list = list(c.fetchall())
    for i in station_list:
        name = i[1]
        names.append(name)
        spelled_name = i[5]
        spelled.append(spelled_name)
        height_list.append(i[7])
        width_list.append(i[8])
        x_list.append(i[9])
        y_list.append(i[10])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])
        color_list.append(i[16])
    get_color_data_sql = "SELECT * FROM currentColor WHERE room = %s"
    c.execute(get_color_data_sql, room)
    color_data_to_list = list(c.fetchall())
    for l in color_data_to_list:
        color = l[2]
        is_available = l[4]
    # Close database connection.
    connection.close()
    return render_template('minethis.html', color=color, time_doubler=time_doubler,
                           is_available=is_available, collected_mine=collected_mine,
                           stationListed=names, spelled=spelled, station=station,
                           message_bomb=message_bomb, room=room,
                           this_room_collected=this_room_collected,
                           width_list=width_list, height_list=height_list, x_list=x_list,
                           y_list=y_list, image_list=image_list, bh_list=bh_list,
                           bw_list=bw_list, br_list=br_list, color_list=color_list,
                           color_selected_list=color_selected_list)


# count_hack = 0
# # Harvest station data
# @app.route('/minethis/<app_id>', methods=['GET', 'POST'])
# def mine_this(app_id):
#     connection = data_connect()
#     c = connection.cursor()
#     room = app_id
#     names = []
#     spelled = []
#     height_list = []
#     width_list = []
#     x_list = []
#     y_list = []
#     image_list = []
#     bh_list = []
#     bw_list = []
#     br_list = []
#     color_selected_list = []
#     color_list = []
#     this_room_collected = "no"
#     collected_mine = "no"
#     color = "Red"
#     station = ""
#     currency = 0
#     is_available = "Yes"
#
#     global count_hack
#     count_hack += 1
#     count_mpd = count_hack % 40
#     if count_mpd > 20:
#         is_available = "No"
#
#     if room == "1":
#         station = "MTR1"
#     if room == "2":
#         station = "MTR2"
#     time_doubler = time_doubler_check(station)
#     message_bomb = looser_check()
#     return render_template('minethis.html', color=color, time_doubler=time_doubler,
#                                       is_available=is_available, collected_mine=collected_mine,
#                                       stationListed=names, spelled=spelled, station=station,
#                                       message_bomb=message_bomb, room=room,
#                                       this_room_collected=this_room_collected,
#                                       width_list=width_list, height_list=height_list, x_list=x_list,
#                                       y_list=y_list, image_list=image_list, bh_list=bh_list,
#                                       bw_list=bw_list, br_list=br_list, color_list=color_list,
#                                       color_selected_list=color_selected_list)


# Harvest station template
@app.route('/minethistemplate/<app_id>')
def mine_this_template(app_id):
    room = app_id
    return render_template('minethistemplate.html', room=room)


# Steal station data
@app.route('/minethat/<app_id>', methods=['GET', 'POST'])
def mine_that(app_id):
    connection = data_connect()
    c = connection.cursor()
    room = app_id
    names = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []
    this_room_collected = "no"
    collected_mine = "no"
    color = "none"
    station = ""
    currency = 0
    atkroom = "2"
    is_available = "Yes"
    if room == "1":
        station = "MOR1"
        atkroom = "2"
    if room == "2":
        station = "MOR2"
        atkroom = "1"
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    if request.method == 'POST':
        station_check = request.form['station']
        check_station_sql = "SELECT * FROM currentColor WHERE station = %s"
        c.execute(check_station_sql, station_check)
        row_count = c.rowcount
        if row_count != 0:
            update_mine_sql = "UPDATE currentColor SET roomCollected = %s, collected = %s WHERE station = %s"
            c.execute(update_mine_sql, (room, "Yes", station_check))
            get_cur_to_add_sql = "SELECT * FROM currency WHERE room = %s"
            c.execute(get_cur_to_add_sql, room)
            get_cur_to_add = list(c.fetchall())
            for i in get_cur_to_add:
                check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s"
                c.execute(check_dual_sql, (room, "2"))
                row_count = c.rowcount
                if row_count != 0:
                    currency = int(i[1]) + 3
                else:
                    currency = int(i[1]) + 2
                try:
                    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s"
                    c.execute(check_dual_sql, (room, "18"))
                    row_count = c.rowcount
                    if row_count != 0:
                        get_hac_to_add_sql = "SELECT * FROM hacks WHERE team = %s"
                        c.execute(get_hac_to_add_sql, room)
                        get_hac_to_add = list(c.fetchall())
                        for f in get_hac_to_add:
                            hacks = int(f[2]) + 1
                            add_hac_sql = "UPDATE hacks SET howMany = %s WHERE team = %s;"
                            c.execute(add_hac_sql, (hacks, room))
                    else:
                        pass
                except InternalError:
                    pass
                if color == "green":
                    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s"
                    c.execute(check_dual_sql, (room, "3"))
                    row_count = c.rowcount
                    if row_count != 0:
                        currency = currency + 3
                if color == "red":
                    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s"
                    c.execute(check_dual_sql, (room, "4"))
                    row_count = c.rowcount
                    if row_count != 0:
                        currency = currency + 3
                if color == "yellow":
                    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s"
                    c.execute(check_dual_sql, (room, "5"))
                    row_count = c.rowcount
                    if row_count != 0:
                        currency = currency + 3

            add_cur_sql = "UPDATE currency SET amount = %s WHERE room = %s;"
            c.execute(add_cur_sql, (currency, room))

            play_add_sql = "INSERT INTO audiomanager (whattoplay, room) VALUES (%s, %s)"
            c.execute(play_add_sql, ("steal", room))
        else:
            insert_lock = "INSERT INTO mineLockOut (station) VALUES (%s);"
            c.execute(insert_lock, station)

    mine_collected_sql = "SELECT * FROM currentColor WHERE room = %s AND collected = %s"
    c.execute(mine_collected_sql, (atkroom, "Yes"))
    row_count_mined = c.rowcount
    if row_count_mined != 0:
        collected_mine = "yes"
        mine_collected_room_sql = "SELECT * FROM currentColor WHERE roomCollected = %s AND room = %s"
        c.execute(mine_collected_room_sql, (room, atkroom))
        row_count_mined_room = c.rowcount
        if row_count_mined_room == 0:
            this_room_collected = "no"
        else:
            this_room_collected = "yes"

    check_lockout_sql = "SELECT * FROM  mineLockOut WHERE station = %s;"
    c.execute(check_lockout_sql, station)

    row_count = c.rowcount
    if row_count != 0:
        station_check_list = list(c.fetchall())
        for j in station_check_list:
            time_to_unlock = j[2]
            time_now = datetime.now()
            elapsed_time = time_now - time_to_unlock
            if elapsed_time.total_seconds() > 30:
                remove_lockout = "DELETE FROM mineLockOut WHERE station = %s"
                c.execute(remove_lockout, station)
            else:
                is_available = "Yes"
                connection.close()
                return render_template('minethis.html', color=color, time_doubler=time_doubler,
                                       is_available=is_available, collected_mine=collected_mine,
                                       stationListed=names, spelled=spelled, station=station,
                                       room=room, message_bomb=message_bomb,
                                       this_room_collected=this_room_collected,
                                       width_list=width_list, height_list=height_list, x_list=x_list,
                                       y_list=y_list, image_list=image_list, bh_list=bh_list,
                                       bw_list=bw_list, br_list=br_list, color_list=color_list,
                                       color_selected_list=color_selected_list)

    station_list_sql = 'SELECT * FROM stationList WHERE room = %s AND is_visible = TRUE;'
    c.execute(station_list_sql, atkroom)
    station_list = list(c.fetchall())
    for i in station_list:
        name = i[1]
        names.append(name)
        spelled_name = i[5]
        spelled.append(spelled_name)
        height_list.append(i[7])
        width_list.append(i[8])
        x_list.append(i[9])
        y_list.append(i[10])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])
        color_list.append(i[16])
    get_color_data_sql = "SELECT * FROM currentColor WHERE room = %s"
    c.execute(get_color_data_sql, atkroom)
    color_data_to_list = list(c.fetchall())
    for l in color_data_to_list:
        color = l[2]
        is_available = l[4]
    # Close database connection.
    connection.close()
    return render_template('minethis.html', color=color, time_doubler=time_doubler,
                           is_available=is_available, collected_mine=collected_mine,
                           stationListed=names, spelled=spelled, station=station,
                           message_bomb=message_bomb, room=room,
                           this_room_collected=this_room_collected,
                           width_list=width_list, height_list=height_list, x_list=x_list,
                           y_list=y_list, image_list=image_list, bh_list=bh_list,
                           bw_list=bw_list, br_list=br_list, color_list=color_list,
                           color_selected_list=color_selected_list)


# Steal station template
@app.route('/mineothertemplate/<app_id>')
def mine_other_template(app_id):
    room = app_id
    return render_template('mineothertemplate.html', room=room)


# Game pages Ends


# Game managers
# Audio_add accepts posts with a from field of toplay and adds them to the to play database to play on Mirror station
@app.route('/audioadd/<room>/', methods=['GET', 'POST'])
def audio_add(room):
    if request.method == 'POST':
        to_play = request.form['toplay']
        connection = data_connect()
        c = connection.cursor()

        try:
            play_add_sql = "INSERT INTO audiomanager (whattoplay, room) VALUES (%s, %s)"
            c.execute(play_add_sql, (to_play, room))
        except InternalError:
            pass

        connection.close()
    return "Nothing Here"


# audio_check is used by mirror to check if audio needs to be played
@app.route('/audiocheck/<room>')
def audio_check(room):
    tracks = []
    connection = data_connect()
    c = connection.cursor()
    get_audio_sql = "SELECT * FROM audiomanager WHERE room = %s"
    c.execute(get_audio_sql, room)
    audio_list = list(c.fetchall())
    for i in audio_list:
        tracks.append(i[1])
    remove_audio_que = "DELETE FROM audiomanager WHERE room = %s"
    c.execute(remove_audio_que, room)

    connection.close()
    return render_template('audiocheck.html', tracks=tracks)


# hacked buttons
@app.route('/hack_load/')
def hack_load():
    return render_template('hack_load.html')


# currency_func us used on stations that need to check currencies it includes energy, hacks and bomb count
@app.route('/currency/<app_id>', methods=['GET', 'POST'])
def currency_func(app_id):
    connection = data_connect()
    c = connection.cursor()
    hacks_available = 0
    bombs = 0
    opcurrency = 0
    currencies = 0
    room = app_id
    timetodetonate = "-1"
    # Room data
    attack_room = ""
    if room == "1":
        attack_room = "2"
    if room == "2":
        attack_room = "1"

    # Current rooms currency
    currencysql = 'SELECT * FROM currency WHERE room=%s'
    c.execute(currencysql, room)
    currencyget = list(c.fetchall())
    for i in currencyget:
        currencies = i[1]

    # Current rooms currency
    getopcurrencysql = "SELECT * FROM currency WHERE room = %s"
    c.execute(getopcurrencysql, attack_room)
    getcurrencylist = list(c.fetchall())
    for i in getcurrencylist:
        opcurrency = i[1]

    # How many bombs can be deployed that have been bought from the AH
    numberofbombssql = 'SELECT * FROM numberOfBombs WHERE room = %s'
    c.execute(numberofbombssql, room)
    numberofbombs = list(c.fetchall())
    for i in numberofbombs:
        bombs = i[2]

    stationlistsql = 'SELECT * FROM stationList WHERE room = %s'
    c.execute(stationlistsql, room)
    stationlist2 = list(c.fetchall())

    # list off all stations
    # stationlistsql = 'SELECT * FROM stationList WHERE room = %s'
    # c.execute(stationlistsql, attack_room)
    # stationlist = list(c.fetchall())
    #
    # # timer for bombs deployed
    # for i in stationlist:
    #     name = i[1]
    #     stationsbombedsql = 'SELECT * FROM bombsDeployed WHERE stationName = %s'
    #     c.execute(stationsbombedsql, name)
    #     stationsbombed = list(c.fetchall())
    #     for j in stationsbombed:
    #         a = j[3]
    #         b = datetime.now()
    #         timediff = (b - a).seconds
    #         # print("timeDiff = " + str(timeDiff))
    #
    #         if 0 <= timediff <= 30:
    #             timetodetonate = str(30 - timediff)
    #         # print(str(timeDiff))
    #         else:
    #             pass
    stationsbombedsql = 'SELECT * FROM bombsDeployed WHERE room = %s'
    c.execute(stationsbombedsql, attack_room)
    stationsbombed = list(c.fetchall())
    for j in stationsbombed:
        if j[5]:
            a = j[5]
            b = datetime.now()
            if a > b - timedelta(seconds=2):
                timetodetonate = str((a - b).seconds)
                if (a - b).seconds > 100:
                    timetodetonate = "0"
        # print("timeDiff = " + str(timeDiff))

    hacklistsql = "SELECT * FROM hacks WHERE team = %s"
    c.execute(hacklistsql, room)
    hack_list = list(c.fetchall())
    for i in hack_list:
        hacks_available = i[2]

    # close database and render the page
    connection.close()
    return render_template('currency.html', hacksAvailable=hacks_available,
                           opCurrency=opcurrency, currencys=currencies,
                           bombs=bombs, timeToDetonate=timetodetonate, stationlist2=stationlist2)


# This is a fix for the listen station to cut the audio.
@app.route('/hackCheck2/<app_id>')
def hack_check_2(app_id):
    hack_check = "clean"
    connection = data_connect()
    c = connection.cursor()
    station_room = app_id
    block_hack = "14"
    get_quantity_available = "SELECT * FROM marketOwned WHERE itemID = %s AND station=%s"
    c.execute(get_quantity_available, (block_hack, station_room))
    row_count = c.rowcount
    if row_count != 0:
        hack_check = "clean"
    else:
        try:
            hack_check_sql = "SELECT * FROM  hackCheck WHERE roomstation = %s"
            c.execute(hack_check_sql, station_room)
            hack_check_fetch = list(c.fetchall())
            for i in hack_check_fetch:
                hack_check = i[2]
        except InternalError:
            hack_check = "clean"

    # Close database connection.
    connection.close()
    return render_template('hackCheck2.html', hackCheck=hack_check)


# hack_check_func checks is stations are hacked it is used on all stations
@app.route('/hackCheck/<app_id>')
def hack_check_func(app_id):
    hack_check = "clean"
    connection = data_connect()
    c = connection.cursor()
    station_room = app_id
    block_hack = "14"
    get_quantity_available = "SELECT * FROM marketOwned WHERE itemID = %s AND station=%s"
    c.execute(get_quantity_available, (block_hack, station_room))
    row_count = c.rowcount
    if row_count != 0:
        hack_check = "clean"
    else:
        try:
            hack_check_sql = "SELECT * FROM  hackCheck WHERE roomstation = %s"
            c.execute(hack_check_sql, station_room)
            hack_check_fetch = list(c.fetchall())
            for i in hack_check_fetch:
                hack_check = i[2]
        except InternalError:
            hack_check = "clean"

    # Close database connection.
    connection.close()
    return render_template('hackCheck.html', hackCheck=hack_check)


# count_hack = 0
# # hack_check_func checks is stations are hacked it is used on all stations
# @app.route('/hackCheck/<app_id>')
# def hack_check_func(app_id):
#     global count_hack
#     count_hack += 1
#     hack_check = "clean"
#     count_mpd = count_hack % 40
#     if count_mpd > 20:
#         hack_check = "hacked"
#     print(count_hack)
#     return render_template('hackCheck.html', hackCheck=hack_check)


# sremove removes hacks from stations
@app.route('/sRemove/', methods=['GET', 'POST'])
def sremove():
    connection = data_connect()
    c = connection.cursor()
    update_status = 'DELETE FROM hackCheck  WHERE roomstation = %s'
    c.execute(update_status, (request.form['station']))

    # Close database connection.
    connection.close()
    return "updated"


# sethackbackground should no longer be used
@app.route('/sethackBackground/')
def sethackbackground():
    connection = data_connect()
    c = connection.cursor()
    hack_image_list = []
    hack_back_selector_sql = "SELECT * FROM hackImages"
    c.execute(hack_back_selector_sql)
    hack_image_list_list = list(c.fetchall())
    for i in hack_image_list_list:
        hack_image_list.append(i[1])
    background_hack = choice(hack_image_list)
    background_hack_1 = choice(hack_image_list)
    background_hack_2 = choice(hack_image_list)
    background_hack_3 = choice(hack_image_list)
    connection.close()
    return render_template('setBackgroundhack.html', background_hack=background_hack,
                           background_hack_1=background_hack_1,
                           background_hack_2=background_hack_2, background_hack_3=background_hack_3)


# This sets the color for the light in the center of the room.
@app.route('/middlecolor/<room>')
def middle_color(room):
    connection = data_connect()
    c = connection.cursor()
    color = "none"

    try:
        color_selector_sql = 'SELECT * FROM currentColor WHERE collected = %s AND roomCollected = %s'
        c.execute(color_selector_sql, ("Yes", room))
        color_selector = list(c.fetchall())
        for i in color_selector:
            color = i[2]
    except InternalError:
        pass

    # Close database connection.
    connection.close()
    return render_template('setBackground.html', color=color)


# setbackground sets the lights color of the station lights
@app.route('/setBackground/<station>/<room>')
def setbackground(station, room):
    station_str = str(station)
    connection = data_connect()
    c = connection.cursor()
    colors_list = ["red", "green", "blue"]

    try:
        color_selector_sql = "SELECT * FROM currentColor WHERE room = %s"
        c.execute(color_selector_sql, room)
        color_selector = list(c.fetchall())
        for i in color_selector:
            color_selected = i[2]
            colors_list.remove(color_selected)
    except InternalError:
        pass

    color = choice(colors_list)

    try:
        color_selector_sql = "SELECT * FROM currentColor WHERE station = %s"
        c.execute(color_selector_sql, station_str)
        color_selector = list(c.fetchall())
        for i in color_selector:
            color = i[2]
    except InternalError:
        pass

    # Close database connection.
    connection.close()
    return render_template('setBackground.html', color=color)


# bombcheck is for the geiger counter which is not implemented
@app.route('/bombcheck/<app_id>', methods=['GET', 'POST'])
def bombcheck(app_id):
    room = app_id
    connection = data_connect()
    c = connection.cursor()
    location = "check reader"
    mac = ""
    bomb_located = "False"
    button_active = "true"
    request_method = "else"
    time_to_check = datetime.now()
    time_now = datetime.now()
    get_time_sql = "SELECT * FROM bombDetect WHERE room = %s"
    c.execute(get_time_sql, room)
    get_time_list = list(c.fetchall())
    for i in get_time_list:
        time_to_check = i[3]
    try:
        elapsed_time = time_now - time_to_check
        if elapsed_time.total_seconds() < 60:
            button_active = "false"
    except InternalError:
        pass

    if request.method == 'POST':
        request_method = "POST"
        update_last_check = 'UPDATE bombDetect SET time_checked = %s WHERE room = %s'
        c.execute(update_last_check, (time_now, room))

        bomb_detect_sql = "SELECT * FROM bombDetect WHERE room = %s"
        c.execute(bomb_detect_sql, room)
        bomb_detect_list = list(c.fetchall())
        for i in bomb_detect_list:
            mac = i[1]
        get_detector_location_sql = "SELECT * FROM playerLocation WHERE mac = %s"
        c.execute(get_detector_location_sql, mac)
        get_detector_location = list(c.fetchall())
        for j in get_detector_location:
            location = j[2]
        bomb_locations_sql = "SELECT * FROM bombsDeployed WHERE stationName = %s"
        c.execute(bomb_locations_sql, location)
        row_count = c.rowcount
        if row_count != 0:
            bomb_located = "true"
        else:
            bomb_located = "false"
        bmb_check = "SELECT * FROM bombsDeployed WHERE room=%s"
        c.execute(bmb_check, room)
        row_count = c.rowcount
        if row_count != 0:
            get_time_location_list = list(c.fetchall())
            for i in get_time_location_list:
                time_deployed = i[3]
                time_now = datetime.now()
                elapsed_time = time_now - time_deployed
                if int(elapsed_time.total_seconds()) > 30:
                    bomb_located = "oot"
        elif row_count == 0:
            bomb_located = "oot"

    # Close database connection.
    connection.close()
    return render_template('bombcheck.html', request_method=request_method,
                           button_active=button_active,
                           location=location, bomb_located=bomb_located)


# bomb_detect is bombcheck template
@app.route('/bombDetect/<app_id>', methods=['GET', 'POST'])
def bomb_detect(app_id):
    room = app_id
    return render_template('bombDetect.html', room=room)


@app.route('/calibrationTemplate', methods=['GET', 'POST'])
def calibration_template():
    stationListed = []
    treckersListed = []
    connection = data_connect()
    c = connection.cursor()
    sql_get_station = "SELECT * FROM stationList ORDER BY room, name;"
    c.execute(sql_get_station)
    station_list = list(c.fetchall())
    sql_get_tracker = "SELECT * FROM TrackerNames ORDER BY name;"
    c.execute(sql_get_tracker)
    tracker_list = list(c.fetchall())
    connection.close()
    for tracker in tracker_list:
        treckersListed.append([tracker[1], tracker[2]])
    for station in station_list:
        stationListed.append([station[1], ' '.join([str(station[5]), str(station[2])])])
    return render_template('calibrationTemplate.html', stationListed=stationListed, treckersListed=treckersListed)


@app.route('/distancetemplate', methods=['GET', 'POST'])
def distance_template():
    stationListed = []
    treckersListed = []
    connection = data_connect()
    c = connection.cursor()
    sql_get_station = "SELECT * FROM stationList ORDER BY room, name;"
    c.execute(sql_get_station)
    station_list = list(c.fetchall())
    sql_get_tracker = "SELECT * FROM TrackerNames ORDER BY name;"
    c.execute(sql_get_tracker)
    tracker_list = list(c.fetchall())
    connection.close()
    for tracker in tracker_list:
        treckersListed.append([tracker[1], tracker[2]])
    for station in station_list:
        stationListed.append([station[1], ' '.join([str(station[5]), str(station[2])])])
    return render_template('distanceCalibrataionTemplate.html', stationListed=stationListed,
                           treckersListed=treckersListed)


# function to check if assist is assisting said station
def time_doubler_check(station):
    connection = data_connect()
    c = connection.cursor()
    time_doubler = "no"
    get_time_doubler_sql = "SELECT * FROM timeDoubler WHERE station = %s"
    c.execute(get_time_doubler_sql, station)
    row_count_time = c.rowcount
    if row_count_time != 0:
        time_doubler = "yes"
    connection.close()
    return time_doubler


# check to see if game is in a game over state
def looser_check():
    connection = data_connect()
    c = connection.cursor()
    is_live_sql = "SELECT * FROM isalive"
    c.execute(is_live_sql)
    row_count = c.rowcount
    if row_count != 0:
        connection.close()
        return "exit"
    get_looser_sql = "SELECT * FROM loosingTeam"
    c.execute(get_looser_sql)
    row_count = c.rowcount
    if row_count != 0:
        connection.close()
        return "exit"
    else:
        connection.close()
        return ""


# sets favicon to prevent chrome from showing an error for no favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# API
# ipaddresses gets the stations ip addresses and stores them
@app.route('/ipaddresses', methods=['GET', 'POST'])
def ipaddresses():
    if request.method == 'POST':
        connection = data_connect()
        c = connection.cursor()
        station_name = request.form['station']
        ipaddress = request.form['ip']
        try:
            update_sql = "INSERT INTO station_ips (station, ipaddress, reboot) " \
                         "VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE station = %s, ipaddress = %s;"
            c.execute(update_sql, (station_name, ipaddress, "0", station_name, ipaddress))
            reboot_check = "SELECT * FROM station_ips WHERE station = %s"
            c.execute(reboot_check, station_name)
            reboot_checker = list(c.fetchall())
            for k in reboot_checker:
                reboot_checked = k[3]
                if reboot_checked == 1:
                    reboot_change = "UPDATE station_ips SET reboot = %s WHERE station = %s"
                    c.execute(reboot_change, ("0", station_name))
                    connection.close()
                    return "reboot"
        except InternalError:
            pass
        connection.close()
        return "ip accepted"
    return "ip not accepted"


# bleraw accepts raw BLE data sent from the PI's showing the signal strength station
# then stores the data to trackers
@app.route('/bleraw', methods=['GET', 'POST'])
def bleraw():
    if request.method != 'POST':
        return "mac not accepted"

    ts = time.time()
    station_name = request.form['station']
    bt_addr = request.form['bt_addr']
    rssi = request.form['rssi']
    tx_power = None
    if 'tx_power' in request.form:
        tx_power = request.form['tx_power']
    if tx_power is not None:
        tx_power = int(float(tx_power))

    room = request.form['room']

    connection = data_connect()
    c = connection.cursor()
    try:
        insert_sql = "INSERT INTO trackers_raw(moment, rssi, tx_power, beacon_mac, room, station) " \
                     "VALUES (from_unixtime(%s)  ,   %s,       %s,         %s,   %s, %s) "
        c.execute(insert_sql, (ts, int(float(rssi)), tx_power, bt_addr, room, station_name))
    except Exception as e:
        print("Occured exception ", e)

    connection.close()
    return "accepted"


# bledata accepts the BLE data sent from the PI's showing the signal strength station then stores the data to trackers
@app.route('/bledata', methods=['GET', 'POST'])
def bledata():
    if request.method == 'POST':
        connection = data_connect()
        c = connection.cursor()
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        station_name = request.form['station']
        bt_addr = request.form['bt_addr']
        avg = request.form['avg']
        room = request.form['room']
        if 'packet_data' in request.form:
            packet_data = request.form['packet_data']
            properties = request.form['properties']
        else:
            packet_data = ""
            properties = ""
        # TODO: update
        if 'packet' in request.form:
            logger.debug(request.form['packet'])
        macstat = str(bt_addr) + "," + str(station_name)

        if rssi_name in request.form and use_rssi:
            # rssi = request.form['rssi_window']
            rssi = request.form[rssi_name]
            if bt_addr in rssi_buffer[station_name]:
                avg2 = computeDistance(float(rssi), rssi_buffer[station_name][bt_addr])
                # avg2 = computeDistance(float(rssi), -60)
            else:
                avg2 = computeDistance(float(rssi), -65)
            avg = float(avg2)

        if 'rssi_filter' in request.form:
            try:
                ts = time.time()
                timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                kalman_value = request.form['rssi_filter']
                sql_request = "INSERT INTO temp_calibration (mac, station, tx_power, timestamp) VALUES (%s, %s, %s, %s);"
                c.execute(sql_request, (bt_addr, station_name, kalman_value, timestamp))
                delta_time = datetime.now() - timedelta(minutes=1)
                sql_request_remove = "DELETE FROM temp_calibration WHERE timestamp < %s;"
                c.execute(sql_request_remove, delta_time)
            except:
                # TODO: add log error
                pass

        try:
            update_sql = "INSERT INTO trackers (macstat, mac, station, signal_avg, room, packet_data, properties) " \
                         "VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
                         "macstat = %s, mac = %s, station = %s, signal_avg = %s, room = %s, timestamp = %s, packet_data = %s, properties = %s;"
            c.execute(update_sql, (macstat, bt_addr, station_name, avg, room, packet_data, properties, macstat,
                                   bt_addr, station_name, avg, room, timestamp, packet_data, properties))
            insert_sql = "INSERT INTO trackers_value (mac, station, value) VALUES (%s, %s, %s);"
            c.execute(insert_sql, (bt_addr, station_name, float(avg)))
            # logger.debug(update_sql % (macstat, bt_addr, station_name, avg, room, packet_data, properties, macstat,
            #                        bt_addr, station_name, avg, room, timestamp, packet_data, properties))
        except InternalError as e:
            # TODO: add log error
            pass
        connection.close()
        return "mac accepted"
    return "mac not accepted"


# Game Inactive
# nogame is used on all station when no game is on or the game is in game over state and listens for when a game begins
@app.route('/nogametemplate/<station>')
def nogametemplate(station):
    return render_template("nogametemplate.html", station=station)


@app.route('/nogame/<station>')
def nogame(station):
    connection = data_connect()
    c = connection.cursor()
    message = ""
    status = ""
    blown_up = ""
    get_room_sql = 'SELECT room FROM stationList WHERE name = %s'
    c.execute(get_room_sql, station)
    room_list = list(c.fetchall())
    is_live_sql = "SELECT * FROM isalive WHERE is_alive = 'no'"
    c.execute(is_live_sql)
    row_count = c.rowcount
    if row_count != 0:
        status = "0"
    else:
        getstatus_sql = 'SELECT * FROM loosingTeam'
        c.execute(getstatus_sql)
        row_count = c.rowcount
        if row_count == 0:
            status = "gameon"
        if row_count != 0:
            getstatus_sql = 'SELECT * FROM loosingTeam'
            c.execute(getstatus_sql)
            win_loose = list(c.fetchall())
            for i in win_loose:
                get_name_sql = 'SELECT * FROM stationList WHERE name = %s'
                c.execute(get_name_sql, i[3])
                station_dep = list(c.fetchall())
                for j in station_dep:
                    blown_up = j[5]
            getstatus_sql = 'SELECT * FROM loosingTeam WHERE team = %s'
            c.execute(getstatus_sql, room_list[0])
            row_count_win_lose = c.rowcount

            if row_count_win_lose == 0:
                status = "WIN"
                message = "You blasted the " + blown_up + " station."
            else:
                status = "LOSE"
                message = "You were blasted at the " + blown_up + " station."
    connection.close()

    return render_template("nogame.html", message=message, status=status, station=station)


# Reseters
# reset tracking
@app.route('/resettrackVault', methods=['GET', 'POST'])
def reset_tracking():
    if request.method == 'POST':
        connection = data_connect()
        c = connection.cursor()
        reset_track_data = "TRUNCATE TABLE trackers"
        c.execute(reset_track_data)
        reset_trackers = "TRUNCATE TABLE playerLocation"
        c.execute(reset_trackers)
        connection.close()

        return redirect(url_for('admin'))


# reset all stations
@app.route('/resetallVault', methods=['GET', 'POST'])
def reset_all():
    if request.method == 'POST':
        connection = data_connect()
        c = connection.cursor()
        reset_sql = "UPDATE station_ips SET reboot = %s WHERE reboot != %s"
        c.execute(reset_sql, ("1", "1"))
        connection.close()
        return redirect(url_for('admin'))


# reset specific station
@app.route('/resetstation', methods=['GET', 'POST'])
def reset_station():
    if request.method == 'POST':
        connection = data_connect()
        c = connection.cursor()
        station_to_reset = request.form['station']
        reset_sql = "UPDATE station_ips SET reboot = %s WHERE station = %s"
        c.execute(reset_sql, ("1", station_to_reset))
        connection.close()
        return redirect(url_for('admin'))


# reset server
@app.route('/resetserver', methods=['GET', 'POST'])
def reset_server():
    if request.method == 'POST':
        reset_answer = request.form['reset']
        if reset_answer == "True":
            os.system("sudo reboot")
        return "rebooted"
    return "not rebooted"


# Defense station data
@app.route('/mainstation/<app_id>', methods=['GET', 'POST'])
def defenses_station(app_id):
    connection = data_connect()
    c = connection.cursor()
    room = app_id
    names = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_list = []
    collected_mine = "no"
    is_available = "No"
    station_name = ""
    station_check = ""
    station = "MAN{}".format(room)
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    sql_volume = "SELECT volume from station_volume WHERE station=%s;"
    c.execute(sql_volume, station)
    volume_list = list(c.fetchall())
    volume = volume_list[0][0]

    if request.method == 'POST':
        is_available = "Yes"
        station_check = request.form['station']
        sql_query = "SELECT * FROM bombsDeployed WHERE stationName = %s AND timeIncoming < NOW();"
        c.execute(sql_query, station_check)
        row_count = c.rowcount
        if row_count != 0:
            collected_mine = "yes"
        else:
            collected_mine = "no"
        insert_lock = "INSERT INTO mineLockOut (station) VALUES (%s);"
        c.execute(insert_lock, station)

        station_sql = 'SELECT * FROM stationList WHERE name = %s;'
        c.execute(station_sql, station_check)
        station_list = list(c.fetchall())[0]

        sql_query = "INSERT INTO station_defence (station, room, status, timestamp) " \
                    "VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
                    "station = %s, room = %s, status = %s, timestamp = %s;"
        c.execute(sql_query, (
            station_check, room, collected_mine, datetime.now(), station_check, room, collected_mine, datetime.now()))

        connection.close()
        station_name = station_list[5]

        response = render_template('defenseStation.html', time_doubler=time_doubler,
                                   collected_mine=collected_mine, is_available=is_available,
                                   stationListed=names, station=station,
                                   message_bomb=message_bomb, room=room,
                                   width_list=width_list, height_list=height_list, x_list=x_list,
                                   y_list=y_list, image_list=image_list, bh_list=bh_list,
                                   bw_list=bw_list, br_list=br_list, color_list=color_list,
                                   station_name=station_name, init_station_name='Yes', volume=volume
                                   )
        return response

    check_lockout_sql = "SELECT * FROM  mineLockOut WHERE station = %s;"
    c.execute(check_lockout_sql, station)
    row_count = c.rowcount
    if row_count != 0:
        station_check_list = list(c.fetchall())
        for j in station_check_list:
            time_to_unlock = j[2]
            time_now = datetime.now()
            elapsed_time = time_now - time_to_unlock
            if elapsed_time.total_seconds() > 4:
                remove_lockout = "DELETE FROM mineLockOut WHERE station = %s"
                c.execute(remove_lockout, station)
            else:
                is_available = "Yes"
                connection.close()
            return render_template('defenseStation.html', time_doubler=time_doubler,
                                   collected_mine=collected_mine, volume=volume,
                                   stationListed=names, station=station,
                                   message_bomb=message_bomb, room=room,
                                   width_list=width_list, height_list=height_list, x_list=x_list,
                                   y_list=y_list, image_list=image_list, bh_list=bh_list,
                                   bw_list=bw_list, br_list=br_list, color_list=color_list,
                                   station_name=station_name, is_available=is_available, init_station_name='No')

    defense_list_sql = 'SELECT * FROM station_defence WHERE room = %s;'
    c.execute(defense_list_sql, room)
    defese_list = list(c.fetchall())
    defense_dict = {defence[1]: defence[3] for defence in defese_list}

    station_list_sql = 'SELECT * FROM stationList WHERE room = %s AND lay_bomb=TRUE;'
    c.execute(station_list_sql, room)
    station_list = list(c.fetchall())
    for i in station_list:
        name = i[1]
        names.append(name)
        spelled_name = i[5]
        spelled.append(spelled_name)
        height_list.append(i[7])
        width_list.append(i[8])
        # x_list.append(i[9])
        # y_list.append(i[10])
        x_list.append(i[17])
        y_list.append(i[18])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])

        if name in defense_dict:
            if defense_dict[name] == 'yes':
                color_list.append(i[15])
            else:
                color_list.append(i[23])
        else:
            color_list.append(i[16])

        if name == station_check:
            station_name = spelled_name

    # Close database connection.
    connection.close()
    return render_template('defenseStation.html', time_doubler=time_doubler,
                           collected_mine=collected_mine, is_available=is_available,
                           stationListed=names, station=station,
                           message_bomb=message_bomb, room=room,
                           width_list=width_list, height_list=height_list, x_list=x_list,
                           y_list=y_list, image_list=image_list, bh_list=bh_list,
                           bw_list=bw_list, br_list=br_list, color_list=color_list,
                           station_name=station_name, init_station_name='No', volume=volume)


# Defense station template
@app.route('/maintemplate/<app_id>')
def defenses_template(app_id):
    room = app_id
    return render_template('defensetemplate.html', room=room)


@app.route("/associations", methods=['GET', 'POST'])
def curent_associations():
    connection = data_connect()
    c = connection.cursor()
    name_trackers = []
    if request.method == 'GET':
        row = c.execute("SELECT name FROM game.TrackerNames")
        for i in range(row):
            name_trackers.append(c.fetchone()[0])
        return render_template('page_associations.html', name_tracker = name_trackers)
    if request.method == "POST":
        pass


@app.route('/setvolume', methods=['GET', 'POST'])
def save_volume():
    if request.method == 'POST':
        station = request.form['station']
        volume = request.form['volume']
        update_sql = "UPDATE station_volume SET volume = %s WHERE station = %s"
        connection = data_connect()
        c = connection.cursor()
        c.execute(update_sql, (volume, station))
        connection.close()
    return ""


# @app.route('/blecalibration', methods=['GET', 'POST'])
# def ble_calibration():
#     return ""
#     if request.method == 'POST':
#         ts = time.time()
#         timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#         station_name = request.form['station']
#         bt_addr = request.form['bt_addr']
#         avg = request.form['kalman']
#         connection = data_connect()
#         c = connection.cursor()
#         sql_request = "INSERT INTO temp_calibration (mac, station, tx_power, timestamp) VALUES (%s, %s, %s, %s);"
#         c.execute(sql_request, (bt_addr, station_name, avg, timestamp))
#         delta_time = datetime.now() - timedelta(minutes=1)
#         sql_request_remove = "DELETE FROM temp_calibration WHERE timestamp < %s;"
#         c.execute(sql_request_remove, delta_time)
#         connection.close()
#     return ""


@socketio.on('hackCheck')
def handle_hack(message):
    app_id = message['station']
    hack_check = "clean"
    connection = data_connect()
    c = connection.cursor()
    station_room = app_id
    block_hack = "14"
    get_quantity_available = "SELECT * FROM marketOwned WHERE itemID = %s AND station=%s"
    c.execute(get_quantity_available, (block_hack, station_room))
    row_count = c.rowcount
    if row_count != 0:
        hack_check = "clean"
    else:
        try:
            hack_check_sql = "SELECT * FROM  hackCheck WHERE roomstation = %s"
            c.execute(hack_check_sql, station_room)
            hack_check_fetch = list(c.fetchall())
            for i in hack_check_fetch:
                hack_check = i[2]
        except InternalError:
            hack_check = "clean"

    # Close database connection.
    connection.close()

    if 'status' in message:
        status = "clean"
        if message['status'] == "ON":
            status = "hacked"
        if status == hack_check:
            return
    response = render_template('hackCheck.html', hackCheck=hack_check)
    if 'old_value' in message:
        if message['old_value'] == response:
            return

    emit('hackCheck', response)


@socketio.on('currency')
def handle_hack(message):
    room = message['room']
    connection = data_connect()
    c = connection.cursor()
    hacks_available = 0
    bombs = 0
    opcurrency = 0
    currencies = 0
    timetodetonate = "-1"
    # Room data
    attack_room = ""
    if str(room) == "1":
        attack_room = "2"
    if str(room) == "2":
        attack_room = "1"

    # Current rooms currency
    currencysql = 'SELECT * FROM currency WHERE room=%s'
    c.execute(currencysql, room)
    currencyget = list(c.fetchall())
    for i in currencyget:
        currencies = i[1]

    # Current rooms currency
    getopcurrencysql = "SELECT * FROM currency WHERE room = %s"
    c.execute(getopcurrencysql, attack_room)
    getcurrencylist = list(c.fetchall())
    for i in getcurrencylist:
        opcurrency = i[1]

    # How many bombs can be deployed that have been bought from the AH
    numberofbombssql = 'SELECT * FROM numberOfBombs WHERE room = %s'
    c.execute(numberofbombssql, room)
    numberofbombs = list(c.fetchall())
    for i in numberofbombs:
        bombs = i[2]

    stationlistsql = 'SELECT * FROM stationList WHERE room = %s'
    c.execute(stationlistsql, room)
    stationlist2 = list(c.fetchall())

    # list off all stations
    stationlistsql = 'SELECT * FROM stationList WHERE room = %s'
    c.execute(stationlistsql, attack_room)
    stationlist = list(c.fetchall())

    # timer for bombs deployed
    for i in stationlist:
        name = i[1]
        stationsbombedsql = 'SELECT * FROM bombsDeployed WHERE stationName = %s'
        c.execute(stationsbombedsql, name)
        stationsbombed = list(c.fetchall())
        for j in stationsbombed:
            a = j[3]
            b = datetime.now()
            timediff = (b - a).seconds
            # print("timeDiff = " + str(timeDiff))

            if 0 <= timediff <= 30:
                timetodetonate = str(30 - timediff)
            # print(str(timeDiff))
            else:
                pass
    hacklistsql = "SELECT * FROM hacks WHERE team = %s"
    c.execute(hacklistsql, room)
    hack_list = list(c.fetchall())
    for i in hack_list:
        hacks_available = i[2]

    # close database and render the page
    connection.close()
    response = render_template('currency.html', hacksAvailable=hacks_available,
                               opCurrency=opcurrency, currencys=currencies,
                               bombs=bombs, timeToDetonate=timetodetonate, stationlist2=stationlist2)
    if 'old_value' in message:
        if message['old_value'] == response:
            return
    emit('currency', response)


@socketio.on('cameraStation')
def handle_camearstation(message):
    station = message['station']
    room = message['room']
    connection = data_connect()
    c = connection.cursor()
    atkroom = "0"
    timer_message = ""

    if str(room) == "1":
        atkroom = "2"
    if str(room) == "2":
        atkroom = "1"

    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    check_dual_sql = "SELECT * FROM marketOwned WHERE team = %s AND itemID = %s;"
    c.execute(check_dual_sql, (room, "6"))
    row_count = c.rowcount

    if row_count != 0:
        cams_available = "2"
    else:
        cams_available = "1"

    get_quantity_available = "SELECT * FROM marketOwned WHERE itemID = %s AND " \
                             "team=%s AND time_bought BETWEEN NOW() -" \
                             "INTERVAL 5 MINUTE AND NOW()"
    c.execute(get_quantity_available, ("8", atkroom))
    counted_market = c.rowcount
    if counted_market != 0:
        cams_available = "0"
        rows_bloks = list(c.fetchall())
        time_bloks = max([row[7] for row in rows_bloks])
        time_now = datetime.now()
        time_left_sec = 300 - int((time_now - time_bloks).total_seconds())
        timer_message = "YOUR CAMERAS HAVE BEEN SHUT DOWN. {0}:{1:02d} UNTIL THEY ARE BACK ONLINE." \
            .format(time_left_sec // 60, time_left_sec % 60)
    # Close database connection.
    connection.close()
    response = render_template('cameraStation.html', cams_available=cams_available,
                               time_doubler=time_doubler, message_bomb=message_bomb, station=station,
                               timer_message=timer_message)
    if 'old_value' in message:
        if message['old_value'] == response:
            return
    emit('cameraStation', response)


@socketio.on('masterStation')
def handle_masterstation(message):
    connection = data_connect()
    c = connection.cursor()
    room = message['room']
    station = ""
    if str(room) == "1":
        station = "MAS1"
    elif str(room) == "2":
        station = "MAS2"
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    station_listed = []
    doubler_station = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []

    doubler_station_active = ""
    check_doubler_sql = "SELECT * FROM timeDoubler WHERE room = %s"
    c.execute(check_doubler_sql, room)
    check_doubler_list_sql = list(c.fetchall())
    for j in check_doubler_list_sql:
        doubler_station.append(j[1])
    station_list = 'SELECT * FROM stationList WHERE room = %s'
    c.execute(station_list, room)
    station_list_sql = list(c.fetchall())
    for i in station_list_sql:
        spelled.append(i[5])
        height_list.append(i[7])
        width_list.append(i[8])
        x_list.append(i[17])
        y_list.append(i[18])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])
        if len(i) < 24:
            # hot fix, can be deleted after making changes to the database
            color_selected_list.append('#880000; border-style: none; background: transparent !important; border:0 '
                                       '!important; filter: brightness(.50) hue-rotate(150deg)  saturate(5) !important;')
        else:
            color_selected_list.append(i[23])
        color_list.append(i[16])
        if i[1] in doubler_station:
            doubler_station_active = i[1]
            station_listed.append(i[1])
        else:
            station_listed.append(i[1])

    if request.method == 'POST':
        is_time_double_active_sql = "SELECT * FROM timeDoubler WHERE room = %s"
        c.execute(is_time_double_active_sql, room)
        row_count = c.rowcount
        if row_count != 0:
            station_remove = "DELETE FROM timeDoubler WHERE room = %s"
            c.execute(station_remove, room)
        station_insert_sql = "INSERT INTO timeDoubler (station, doubler, room) VALUES (%s, %s, %s)"
        c.execute(station_insert_sql, (request.form['station'], "double", room))

    # Close database connection.
    connection.close()
    response = render_template('masterStation.html', room=room, spelled=spelled,
                               stationListed=station_listed, time_doubler=time_doubler,
                               doublerStationActive=doubler_station_active,
                               message_bomb=message_bomb,
                               width_list=width_list, height_list=height_list, x_list=x_list,
                               y_list=y_list, image_list=image_list, bh_list=bh_list,
                               bw_list=bw_list, br_list=br_list, color_list=color_list,
                               color_selected_list=color_selected_list, station=station)
    if 'old_value' in message:
        if message['old_value'] == response:
            return
    emit('masterStation', response)


@socketio.on('mainstation_old')
def handle_mainstation(message):
    connection = data_connect()
    c = connection.cursor()
    room = message['room']
    station_listed = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_selected_list = []
    color_list = []
    station = ""
    if str(room) == "1":
        station = "MAN1"
    elif str(room) == "2":
        station = "MAN2"
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    station_list = "SELECT * FROM stationList WHERE room = %s"
    c.execute(station_list, room)
    station_list_sql = list(c.fetchall())
    for i in station_list_sql:
        if i[1] != "MAN1" and i[1] != "AUD1" and i[1] != "MAN2" and i[1] != "AUD2" \
                and i[1] != "CS21" and i[1] != "CS22":
            station_listed.append(i[1])
            spelled.append(i[5])
            height_list.append(i[7])
            width_list.append(i[8])
            x_list.append(i[17])
            y_list.append(i[18])
            image_list.append(i[11])
            bh_list.append(i[12])
            bw_list.append(i[13])
            br_list.append(i[14])
            color_selected_list.append(i[15])
            color_list.append(i[16])
    connection.close()
    response = render_template('mainstation.html', room=room, spelled=spelled,
                               message_bomb=message_bomb, stationListed=station_listed,
                               time_doubler=time_doubler, width_list=width_list,
                               height_list=height_list, x_list=x_list,
                               y_list=y_list, image_list=image_list, bh_list=bh_list,
                               bw_list=bw_list, br_list=br_list, color_list=color_list,
                               color_selected_list=color_selected_list, station=station)
    if 'old_value' in message:
        if message['old_value'] == response:
            return
    emit('mainstation_old', response)


@socketio.on('audiocheck')
def handle_audio_check(message):
    tracks = []
    room = message['room']
    connection = data_connect()
    c = connection.cursor()
    get_audio_sql = "SELECT * FROM audiomanager WHERE room = %s"
    c.execute(get_audio_sql, room)
    audio_list = list(c.fetchall())
    if not audio_list:
        return
    for i in audio_list:
        tracks.append(i[1])
    remove_audio_que = "DELETE FROM audiomanager WHERE room = %s"
    c.execute(remove_audio_que, room)

    connection.close()
    response = render_template('audiocheck.html', tracks=tracks)
    emit('audiocheck', response)


@socketio.on('audioStation')
def handle_audio_station(message):
    connection = data_connect()
    c = connection.cursor()
    room = message['room']
    if str(room) == '1':
        station = "AUD1"
    elif str(room) == '2':
        station = "AUD2"
    else:
        station = "error"
    message_bomb_20_sec = ""
    message_out = ""
    # Create list of bombs attacking this room if in the air show.
    bmb_check = "SELECT * FROM bombsDeployed WHERE room=%s"
    c.execute(bmb_check, room)
    row_count = c.rowcount
    if row_count != 0:
        get_time_location_list = list(c.fetchall())
        for i in get_time_location_list:
            time_deployed = i[3]
            time_now = datetime.now()

            # Check
            # elapsed_time = time_now - time_deployed
            # if 30 > abs(int(elapsed_time.total_seconds())) > 10:
            #     elapsed_time_reverse = (int(elapsed_time.total_seconds()) - 30) * (-1)
            #     message_bomb_20_sec = "BLAST INCOMING IN {0} SECONDS.".format(str(elapsed_time_reverse))
            # Check
            elapsed_time = time_deployed - time_now
            if 21 > int(elapsed_time.total_seconds()) > -1:
                elapsed_time_reverse = int(elapsed_time.total_seconds())
                message_bomb_20_sec = "BLAST INCOMING IN {0} SECONDS.".format(str(elapsed_time_reverse))

    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()
    connection.close()

    response = render_template('audiostation.html', room=room, station=station,
                               message_bomb_20_sec=message_bomb_20_sec,
                               time_doubler=time_doubler, message_bomb=message_bomb,
                               message_out=message_out)
    if 'old_value' in message:
        if message['old_value'] == response:
            return
    emit('audioStation', response)


# Defense station data
@socketio.on('mainstation')
def handle_defence_station(message):
    connection = data_connect()
    c = connection.cursor()
    room = message['room']
    names = []
    spelled = []
    height_list = []
    width_list = []
    x_list = []
    y_list = []
    image_list = []
    bh_list = []
    bw_list = []
    br_list = []
    color_list = []
    station_name = message['stationCheck']
    stationNameTemp = message['stationNameTemp']
    station_check = ""
    collected_mine = "no"
    is_available = "No"
    station = "MAN{}".format(room)
    time_doubler = time_doubler_check(station)
    message_bomb = looser_check()

    sql_volume = "SELECT volume from station_volume WHERE station=%s;"
    c.execute(sql_volume, station)
    volume_list = list(c.fetchall())
    volume = volume_list[0][0]

    check_lockout_sql = "SELECT * FROM  mineLockOut WHERE station = %s;"
    c.execute(check_lockout_sql, station)
    row_count = c.rowcount
    if row_count != 0:
        station_check_list = list(c.fetchall())
        for j in station_check_list:
            time_to_unlock = j[2]
            time_now = datetime.now()
            elapsed_time = time_now - time_to_unlock

            sql_query = 'SELECT * FROM stationList WHERE name = %s;'
            c.execute(sql_query, stationNameTemp)
            station_list = list(c.fetchall())
            if station_list:
                station_name = station_list[0][5]

            if elapsed_time.total_seconds() > 4:
                remove_lockout = "DELETE FROM mineLockOut WHERE station = %s"
                c.execute(remove_lockout, station)
                continue
            else:
                is_available = "Yes"

            sql_query = "SELECT * FROM bombsDeployed WHERE stationName = %s AND timeIncoming < NOW();"
            c.execute(sql_query, stationNameTemp)
            row_count = c.rowcount
            if row_count != 0:
                collected_mine = "yes"
            else:
                collected_mine = "no"

            connection.close()
            response = render_template('defenseStation.html', time_doubler=time_doubler,
                                       collected_mine=collected_mine,
                                       stationListed=names, station=station,
                                       message_bomb=message_bomb, room=room,
                                       width_list=width_list, height_list=height_list, x_list=x_list,
                                       y_list=y_list, image_list=image_list, bh_list=bh_list,
                                       bw_list=bw_list, br_list=br_list, color_list=color_list, volume=volume,
                                       station_name=station_name, is_available=is_available, init_station_name='No')

            if 'old_value' in message:
                if message['old_value'] == response:
                    return
            emit('mainstation', response)
            return

    defense_list_sql = 'SELECT * FROM station_defence WHERE room = %s;'
    c.execute(defense_list_sql, room)
    defese_list = list(c.fetchall())
    defense_dict = {defence[1]: defence[3] for defence in defese_list}

    station_list_sql = 'SELECT * FROM stationList WHERE room = %s AND lay_bomb=TRUE;'
    c.execute(station_list_sql, room)
    station_list = list(c.fetchall())
    for i in station_list:
        name = i[1]
        names.append(name)
        spelled_name = i[5]
        spelled.append(spelled_name)
        height_list.append(i[7])
        width_list.append(i[8])
        # x_list.append(i[9])
        # y_list.append(i[10])
        x_list.append(i[17])
        y_list.append(i[18])
        image_list.append(i[11])
        bh_list.append(i[12])
        bw_list.append(i[13])
        br_list.append(i[14])
        if name in defense_dict:
            if defense_dict[name] == 'yes':
                color_list.append(i[15])
            else:
                color_list.append(i[23])
        else:
            color_list.append(i[16])

        if name == station_check:
            station_name = spelled_name
        if name == station_check:
            station_name = spelled_name

    # Close database connection.
    connection.close()
    response = render_template('defenseStation.html', time_doubler=time_doubler,
                               collected_mine=collected_mine, volume=volume,
                               stationListed=names, station=station,
                               message_bomb=message_bomb, room=room,
                               width_list=width_list, height_list=height_list, x_list=x_list,
                               y_list=y_list, image_list=image_list, bh_list=bh_list,
                               bw_list=bw_list, br_list=br_list, color_list=color_list,
                               station_name=station_name, is_available=is_available, init_station_name='No')
    if 'old_value' in message:
        if message['old_value'] == response:
            return
    emit('mainstation', response)


@socketio.on('calibration')
def handle_calibration(message):
    mac = message['tracker']
    station = message['station']
    # TODO: add save val

    current_val = rssi_buffer[station][mac]

    connection = data_connect()
    c = connection.cursor()

    sql_get_new_valibrate = "SELECT * FROM temp_calibration WHERE station=%s AND mac = %s ORDER BY timestamp DESC LIMIT 1;"
    c.execute(sql_get_new_valibrate, (station, mac))
    result = list(c.fetchall())

    if not result:
        new_val = None
    else:
        new_val = result[0][3]

    if message.get('save_value', False) and new_val is not None and new_val != current_val:
        sql_request = """
        UPDATE tracker_calibration SET tx_power=%s WHERE mac=%s AND station=%s;
        """
        result = c.execute(sql_request, (new_val, mac, station))
        if result == 0:
            sql_request = "INSERT INTO tracker_calibration (mac, station, tx_power) VALUES (%s, %s, %s);"
            c.execute(sql_request, (mac, station, new_val))
        rssi_buffer[station][mac] = new_val
        connection.close()
        return
    connection.close()
    response = {"current_val": str(current_val), "new_val": str(new_val)}
    emit('calibration', response)


@socketio.on('calibrationDistance')
def handle_calibration(message):
    mac = message.get('tracker', None)
    station = message.get('station', None)
    distance = message.get('distance', None)

    connection = data_connect()
    c = connection.cursor()

    sql_get_new_valibrate = "SELECT * FROM temp_calibration WHERE station=%s AND mac = %s ORDER BY timestamp DESC LIMIT 1;"
    c.execute(sql_get_new_valibrate, (station, mac))
    result = list(c.fetchall())

    if not result:
        new_val = None
    else:
        new_val = result[0][3]

    if message.get('save_value', False) and new_val is not None:
        # TODO: check values
        sql_request = "INSERT INTO distance_value (mac, station, tx_power, distance) VALUES (%s, %s, %s, %s);"
        c.execute(sql_request, (mac, station, new_val, distance))
        rssi_buffer[station][mac] = new_val
        connection.close()
        return

    if message.get('drop_table', False):
        # TODO: test code
        print('drop_table')
        sql_request = "TRUNCATE TABLE distance_value;"
        c.execute(sql_request)
        connection.close()
        return

    if message.get('coefficient_calculation', False):
        # TODO: test code
        compute_coef()
        print('coefficient_calculation')
        # TODO: compute coefficient
        connection.close()
        return

    connection.close()
    response = {"new_val": str(new_val)}
    emit('calibrationDistance', response)


def set_logger_file():
    log_dir = "./log"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # logger.basicConfig(filename=file_log, filemode='a', level=getattr(logging, "DEBUG"),
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.config.fileConfig('logging.conf')
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.ERROR)
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    fil_log = os.path.join(log_dir, "track.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.FileHandler(fil_log, mode='w')
    ch.setFormatter(formatter)
    # ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)


def computeDistance(rssi, txPower=-65, k=meter_to_feet):
    if rssi == 0:
        return -1  # if we cannot determine accuracy, return -1.

    ratio = rssi / txPower

    if ratio <= 1.0:
        return np.power(ratio, 10) * k
    else:
        # return math.pow(ratio, 10)
        # TODO: get coef from table?
        return (A * np.power(ratio, B) + C) * k


def init_buffer():
    connection = data_connect()
    c = connection.cursor()

    sql_get_station = "SELECT name FROM stationList;"
    c.execute(sql_get_station)
    station_list = [x[0] for x in c.fetchall()]

    sql_get_tracker = "SELECT mac FROM TrackerNames;"
    c.execute(sql_get_tracker)
    tracker_list = [x[0] for x in c.fetchall()]

    map_rssi = np.zeros((len(station_list), len(tracker_list)))
    map_rssi[:, :] = np.nan

    sql_get_rssi = "SELECT * FROM tracker_calibration;"
    c.execute(sql_get_rssi)
    rssi_list = list(c.fetchall())
    connection.close()
    for rssi_row in rssi_list:
        mac = rssi_row[1]
        station = rssi_row[2]
        tx_power = rssi_row[3]
        i = station_list.index(station)
        j = tracker_list.index(mac)
        map_rssi[i, j] = tx_power

    if np.sum(np.logical_not(np.isnan(map_rssi))) > 0:
        mean_row = np.nanmean(map_rssi, axis=1)
        mean_column = np.nanmean(map_rssi, axis=0)
        mean_rssi = np.nanmean(map_rssi)

        for i, j in zip(*np.where(np.isnan(map_rssi))):
            if not np.isnan(mean_column[j]):
                map_rssi[i, j] = mean_column[j]
            elif not np.isnan(mean_row[i]):
                map_rssi[i, j] = mean_row[i]
            else:
                map_rssi[i, j] = mean_rssi
    else:
        map_rssi[:, :] = -65

    for i, station in enumerate(station_list):
        for j, mac in enumerate(tracker_list):
            tx_power = map_rssi[i, j]
            if station not in rssi_buffer:
                rssi_buffer[station] = {mac: tx_power}
            else:
                rssi_buffer[station][mac] = tx_power


def func(x, a, b, c):
    return a * np.power(x, b) + c


def compute_coef():
    sql_request = "SELECT distance_value.distance, distance_value.tx_power, tracker_calibration.tx_power FROM distance_value " \
                  "LEFT JOIN tracker_calibration ON distance_value.mac=tracker_calibration.mac;"
    connection = data_connect()
    c = connection.cursor()
    c.execute(sql_request)
    rssi_list = list(c.fetchall())
    connection.close()
    xdata = np.zeros((len(rssi_list),))
    ydata = np.zeros((len(rssi_list),))
    for i, row in enumerate(rssi_list):
        xdata[i] = row[1] / row[2]
        ydata[i] = row[0]
    p0 = (0.89976, 9, 0.111)
    popt, pcov = curve_fit(func, xdata, ydata, p0=p0, maxfev=10000)
    ak, bk, ck = popt.astype(float)
    sql_request = "INSERT INTO coefficient (a, b, c) VALUES (%s, %s, %s);"
    connection = data_connect()
    c = connection.cursor()
    c.execute(sql_request, (float(ak), float(bk), float(ck)))
    connection.close()
    A = ak
    B = bk
    C = ck
    print(ak, bk, ck)


def load_coef():
    try:
        sql_request = "SELECT a, b, c FROM coefficient ORDER BY timestamp DESC LIMIT 1;"
        connection = data_connect()
        c = connection.cursor()
        c.execute(sql_request)
        coef_rows = list(c.fetchall())
        connection.close()
        if coef_rows:
            A = coef_rows[0][0]
            B = coef_rows[0][1]
            C = coef_rows[0][1]
    except:
        pass


# create an instance of the Flask
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
    set_logger_file()
    init_buffer()
    load_coef()
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
