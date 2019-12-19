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

# smoothing window size
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


def get_playrers(c):
    get_players = "SELECT mac, master_name, name from game.TrackerNames;"
    c.execute(get_players)
    listed_players = list(c.fetchall())
    dict_players = {}
    master_players = {}
    for player in listed_players:
        if player[1] in ['', ' '] or player[1] == player[2]:
            master_name = player[2]
            master_players[player[2]] = player[0]
        else:
            master_name = player[1]
        if master_name not in dict_players:
            dict_players[master_name] = list()
        dict_players[master_name].append(player[0])
    return dict_players, master_players


def station_synchronization(mac_map, dict_players, tracker_participation):
    common_stations = []
    trackers = dict_players[tracker_participation[0]]
    station1 = set(mac_map[trackers[0]])
    station2 = set(mac_map[trackers[1]])
    station2.update(station1)
    for station in station2:
        common_stations.append(station)
    return common_stations


def new_loop():
    # get temporary list of worked trackers (need running app.py) !!!
    connection = dataconnect()
    c = connection.cursor()
    get_locations = "SELECT trackers.mac, trackers.station " \
                    "FROM trackers " \
                    "LEFT JOIN TrackerNames " \
                    "ON trackers.mac = TrackerNames.mac " \
                    "where not isnull(TrackerNames.name) AND trackers.station NOT IN ('BMB1', 'BMB2');"

    c.execute(get_locations)
    listed_trackers = list(c.fetchall())

    mac_map = {}
    for k in listed_trackers:  # all trackers!!!
        mac = k[0]
        station = k[1]
        # if mac not in mac_map:
        #     mac_map[mac] = []
        # if station in ['BMB1', 'BMB2']:
        #     continue
        mac_map[mac].append(station)

    mac_location = {}
    mac_mean_value = {}
    mac_mean_rssi = {}
    for mac in mac_map:
        try:
            # list_location = []
            value_array = np.zeros((len(mac_map[mac]), n))
            rssi_array = np.zeros((len(mac_map[mac]), n))
            good_station_index = []
            for i, station in enumerate(mac_map[mac]):
                # if station in ['BMB1', 'BMB2']:
                #     continue
                sql_query = "SELECT value, rssi FROM trackers_value " \
                            "WHERE mac=%s AND station=%s " \
                            "ORDER BY timestamp DESC LIMIT %s;"
                c.execute(sql_query, (mac, station, n))
                listed_value = list(c.fetchall())
                values = [value[0] for value in listed_value]
                rssi = [value[1] for value in listed_value]
                if len(values) < n:
                    value_array[i, :] = MISC_VALUE
                    continue
                good_station_index.append(i)
                value_array[i, :] = values
                rssi_array[i, :] = rssi
            # TODO: remove misc
            list_location = [mac_map[mac][i] for i in good_station_index]
            value_array = value_array[good_station_index, :]
            rssi_array = rssi_array[good_station_index, :]
            mac_location[mac] = list_location
            # dict_station_and_distance = {}
            mean_values = scipy.signal.medfilt(value_array, kernel_size=(1, n))
            mean_rssies = scipy.signal.medfilt(rssi_array, kernel_size=(1, n))
            mac_mean_value[mac] = mean_values[:, n_2]
            mac_mean_rssi[mac] = mean_rssies[:, n_2]
        except:
            pass

    players_location = {}
    players_mean_value = {}
    players_mean_rssi = {}
    players, master_players = get_playrers(c)
    set_mac = set(mac_map.keys())
    for player in players:
        # TODO: merge distance
        set_location = set()
        player_mac = list(set_mac.intersection(players[player]))
        for mac in player_mac:
            set_location.update(mac_location[mac])
        players_location[player] = list(set_location)
        if len(set_location) == 0 or len(player_mac) == 0:
            continue
        player_mean_value = np.zeros((len(players_location[player]), len(player_mac)))*np.nan
        player_mean_rssi = np.zeros((len(players_location[player]), len(player_mac))) * np.nan
        for j, mac in enumerate(player_mac):
            for n_value, station in enumerate(mac_location[mac]):
                i = players_location[player].index(station)
                player_mean_value[i, j] = mac_mean_value[mac][n_value]
                player_mean_rssi[i, j] = mac_mean_rssi[mac][n_value]

        mean_values = np.nanmin(player_mean_value, axis=1)
        players_mean_value[player] = mean_values

        # RSSI type calculation
        mean_rssies = np.nanmin(player_mean_rssi, axis=1)
        players_mean_rssi[player] = mean_rssies

        try:
            locations = players_location[player]
            mean_values = players_mean_value[player]
            mean_rssies = players_mean_rssi[player]

            j = np.nanargmin(mean_values)
            mean_value = mean_values[j]
            location = locations[j]

            j_rssi = np.nanargmin(mean_rssies)
            mean_rssi = mean_rssies[j_rssi]
            location_rssi = locations[j_rssi]

            if triangulate:  # trilateration!
                # location_first = location
                # mean_value_first = mean_value

                if location in locations_room["1"]['stations']:
                    room = "1"
                else:
                    room = "2"

                locs = locations_room[room]['locations']
                stat = locations_room[room]['stations']
                indexs_dist = []
                indexs_locs = []
                for i, loc in enumerate(stat):
                    try:
                        index_dist = locations.index(loc)
                        indexs_locs.append(i)
                        indexs_dist.append(index_dist)
                    except:
                        pass

                if not indexs_locs:
                    continue

                dist_select = mean_values[indexs_dist]
                locs_select = locs[indexs_locs]

                # Select top station
                if TOP_STATION:
                    index_sort = np.argsort(dist_select)
                    index_select = index_sort[:TOP_STATION]
                    dist_select = dist_select[index_select]
                    locs_select = locs_select[index_select, :]

                # Trilateration
                # initial_location = locs_select.mean(axis=0)
                initial_location = locs[stat.index(location)]
                # x = optimization_angle(initial_location, locs_select, dist_select, bounds_room[room]) -- with angle
                x = optimization(initial_location, locs_select, dist_select, bounds_room[room])
                x = x[:2]
                new_dist = cdist(x.reshape((1, 2)), locs)[0, :]

                j = np.argmin(new_dist)
                location = stat[j]
                mean_value = new_dist[j]

            mean_value_str = "{:.2f}".format(mean_value)
            # print(x)
            # print(location, mean_value)
            # print(location_first, location, mean_value-mean_value_first)
            # if location_first != location:
            # 	a = 1
            # if location_first == "MTR1":
            # 	a = 1

            # mac here is not MAC!!! it is station name!!!
            bmb_check = "SELECT * FROM ignorePlayerList WHERE mac = %s;"
            # TODO: check location/mac
            # c.execute(bmb_check, mac)

            mac = master_players[player]
            c.execute(bmb_check, location)
            row_count = c.rowcount
            if row_count == 0:
                insert_location_sql = "INSERT INTO playerLocation (mac, location, bleSignal) " \
                                      "VALUES (%s,%s,%s) ON DUPLICATE KEY " \
                                      "UPDATE mac = %s, location = %s, bleSignal = %s;"
                c.execute(insert_location_sql, (mac, location, mean_value_str,
                                                mac, location, mean_value_str))
        except:
            pass
#    delta_time = datetime.now() - timedelta(minutes=1)
    delta_time = datetime.now() - timedelta(minutes=3)
    if not debug:
        sql_request_remove = "DELETE FROM trackers_value WHERE timestamp < %s;"
        c.execute(sql_request_remove, delta_time)
    connection.close()


def mse(x, locations, distances):
    c_dist = cdist(x.reshape((1, 2)), locations)
    error_dist = distances - c_dist
    error_dist /= distances
    # error_dist[error_dist > 0] = error_dist[error_dist > 0]/2
    mse = np.square(error_dist).mean()
    return mse


def optimization(initial_location, locations, distances, bnds=((0, None), (0, None))):
    result = minimize(
        mse,  # The error function
        initial_location,  # The initial guess
        args=(locations, distances),  # Additional parameters for mse
        method='L-BFGS-B',  # The optimisation algorithm
        options={
            'ftol': 1e-5,  # Tolerance
            'maxiter': 1e+7  # Maximum iterations
        },
        bounds=bnds,
    )
    location = result.x
    return location


def py_ang(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    cosang = np.dot(v1, v2)
    sinang = np.linalg.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)


def mse_angle(x, locations, distances):
    pos = x[:2].reshape((1, 2))
    angle = x[2]
    k = x[3]
    dif_pos = locations - pos
    # TODO: check cos/sin
    direction_vector = np.array((np.cos(angle), np.sin(angle)))

    def func_angle(v):
        return py_ang(v, direction_vector)

    angles = np.apply_along_axis(dif_pos, 1, func_angle)
    angles = np.abs(angles)
    distances_cor = distances.copy()
    distances_cor[angles > np.pi / 2] *= k
    c_dist = cdist(pos, locations)
    error_dist = distances_cor - c_dist
    error_dist /= distances
    mse = np.square(error_dist).mean()
    return mse


def optimization_angle(initial_location, locations, distances, bnds=((0, None), (0, None), (0, 2 * np.pi), (1, 2))):
    initial_location_angle = np.zeros((4,))
    initial_location_angle[:2] = initial_location
    initial_location_angle[2] = np.pi
    initial_location_angle[3] = 1.5
    result = minimize(
        mse_angle,  # The error function
        initial_location,  # The initial guess
        args=(locations, distances),  # Additional parameters for mse
        method='L-BFGS-B',  # The optimisation algorithm
        options={
            'ftol': 1e-5,  # Tolerance
            'maxiter': 1e+7  # Maximum iterations
        },
        bounds=bnds,
    )
    location = result.x
    return location


def compute_bounds():
    for key in locations_room:
        max_val = locations_room[key]['locations'].max(axis=0)
        bounds_room[key] = ((0., max_val[0]), (0., max_val[1]))


def compute_bounds_angles():
    for key in locations_room:
        max_val = locations_room[key]['locations'].max(axis=0)
        bounds_room[key] = ((0., max_val[0]), (0., max_val[1]), (0., 2 * np.pi), (1., 2.))


if __name__ == "__main__":

    if not debug:
        run_once()
    init_locations()

    compute_bounds()  # without angle optimization!!!
    # compute_bounds_angles()  # with angle optimization!!!
    while True:
        # loop()
        new_loop()
