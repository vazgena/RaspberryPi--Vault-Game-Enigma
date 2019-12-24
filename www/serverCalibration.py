from time import sleep
import numpy as np
import scipy.signal
from scipy.spatial.distance import cdist
from scipy.optimize import minimize
from pymysql import InternalError, connect
from datetime import datetime, timedelta
import copy

dbuser = 'game'
dbpass = 'h95d3T7SXFta'

n = 3
# target value, counting from the end. affects lag, -2 recommended
n_2 = -2  # int(np.floor(n/2)) #
triangulate = True
debug = False
TOP_STATION = None

locations_room = {}
bounds_room = {}

MISC_VALUE = 100


# databace connection
def dataconnect():
    return connect(
        db='game',
        user=dbuser,
        passwd=dbpass,
        host='localhost',
        autocommit=True)


def run_once():
    connection = dataconnect()
    c = connection.cursor()
    try:
        track_trunk = "TRUNCATE TABLE trackers"
        c.execute(track_trunk)
        track_trunk = "TRUNCATE TABLE playerLocation"
        c.execute(track_trunk)
    except InternalError:
        pass
    connection.close()


def init_locations():
    connection = dataconnect()
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
        locations_room[str(room)] = {
            "locations": locations,
            "stations": list_stations,
        }

    connection.close()


def loop():
    avg = ""
    saved = []
    connection = dataconnect()
    c = connection.cursor()
    get_locations = "SELECT mac FROM trackers"
    c.execute(get_locations)
    listed_trackers = list(c.fetchall())
    trackers_set = set(listed_trackers)
    listed_unique_trackers = list(trackers_set)

    for k in listed_unique_trackers:
        # TODO: hotfix for BMB1, BMB2
        player_trackers = "SELECT * FROM trackers WHERE mac = %s AND station != 'BMB1' AND station != 'BMB2';"
        c.execute(player_trackers, k)
        compareable_list = list(c.fetchall())
        for l in compareable_list:
            try:
                if l[3] == "BMB1":
                    avg = float(l[4])
                    avg = avg + 2
                else:
                    avg = float(l[4])
                if float(avg) >= float(saved[3]):
                    saved = (l[1], l[2], l[3], avg, l[5])
                else:
                    pass
            except:
                saved = (l[1], l[2], l[3], avg, l[5])
                pass

        try:
            if float(saved[3]) > 60:
                bmb_check = "SELECT * FROM ignorePlayerList WHERE mac = %s"
                c.execute(bmb_check, saved[2])
                row_count = c.rowcount
                if row_count == 0:
                    insert_location_sql = "INSERT INTO playerLocation (mac, location, bleSignal) " \
                                          "VALUES (%s,%s,%s) ON DUPLICATE KEY " \
                                          "UPDATE mac = %s, location = %s, bleSignal = %s"
                    c.execute(insert_location_sql, (saved[1], saved[2], saved[3],
                                                    saved[1], saved[2], saved[3]))
        except:
            print(saved)
            pass
        saved = []

    connection.close()


def calibration_loop(room, tracker_name, location_station):

    return_key = True

    connection = dataconnect()
    c = connection.cursor()

    # Current
    get_score = "SELECT trackers.station, avg(trackers_value.value) as avg_, trackers.mac " \
                "FROM trackers LEFT JOIN TrackerNames ON trackers.mac = TrackerNames.mac, trackers_value " \
                "where not isnull(TrackerNames.name) AND trackers.station NOT IN ('BMB1', 'BMB2') " \
                "and trackers_value.mac=trackers.mac " \
                "and trackers_value.station=trackers.station " \
                "and TrackerNames.name=%s " \
                "group by trackers.station, trackers.mac " \
                "having avg_ > -80;" 

    c.execute(get_score, tracker_name)
    listed_stations = list(c.fetchall())
    current_avg = {}
    mac = ''
    for item in listed_stations:
        station = item[0]
        avg_value = float(item[1])
        current_avg[station] = avg_value
        mac = item[2]

    # Saved
    get_current_calibration = "SELECT tracker_calibration_auto.station, tracker_calibration_auto.tx_power " \
                                "FROM tracker_calibration_auto, TrackerNames, stationList " \
                                "where stationList.name = tracker_calibration_auto.station " \
                                "and TrackerNames.mac=tracker_calibration_auto.mac and TrackerNames.name=%s and stationList.room=%s;"

    c.execute(get_current_calibration, (tracker_name, room))
    saved_calibrations = list(c.fetchall())
    saved_avg = {}
    for item in saved_calibrations:
        station = item[0]
        avg_value = float(item[1])
        saved_avg[station] = avg_value

    # merge
    for item in current_avg:
        station = item
        avg = current_avg[item]

        if item in saved_avg:
            avg = (avg + saved_avg[item]) / 2;
            delta = abs(current_avg[item] - avg)/avg
            print([current_avg[item], saved_avg[item], delta])
        else:
            delta = 1

        if delta >= 0.01:
            renew_sql = "INSERT INTO tracker_calibration_auto (mac, station, tx_power) " \
                                  "VALUES (%s,%s,%s) ON DUPLICATE KEY " \
                                  "UPDATE mac = %s, station = %s, tx_power = %s;"
            c.execute(renew_sql, (mac, station, avg, mac, station, avg))
        else:
            return_key = False

    connection.close()

    return return_key


if __name__ == "__main__":

    room = "1"
    tracker = 'B4'
    location_station = 'MKP1'

    if not debug:
        run_once()
    init_locations()

    key = True
    while key:
        key = calibration_loop(room, tracker, location_station)
