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
TOP_STATION = 3

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


def new_loop():
    # get temporary list of worked trackers (need running app.py) !!!
    connection = dataconnect()
    c = connection.cursor()
    get_locations = "SELECT mac, station FROM trackers;"

    c.execute(get_locations)
    listed_trackers = list(c.fetchall())

    mac_map = {}

    for k in listed_trackers:  # all trackers!!!
        mac = k[0]
        station = k[1]
        if mac not in mac_map:
            mac_map[mac] = []
        if station in ['BMB1', 'BMB2']:
            continue
        mac_map[mac].append(station)

    test_array = np.zeros((40, n))
    mac_location = {}
    mac_mean_value = {}
    num = 0
    for mac in mac_map:
        try:
            value_array = np.zeros((len(mac_map[mac]), n))
            for i, station in enumerate(mac_map[mac]):
                if station in ['BMB1', 'BMB2']:
                    continue
                sql_query = "SELECT value FROM trackers_value WHERE mac=%s AND station=%s ORDER BY timestamp DESC LIMIT %s;"
                c.execute(sql_query, (mac, station, n))
                listed_value = list(c.fetchall())
                values = [value[0] for value in listed_value]
                if len(values) < n:
                    value_array[i, :] = MISC_VALUE
                    continue
                value_array[i, :] = values
                test_array[num, :] = values
                num = num + 1

            mean_values = scipy.signal.medfilt(value_array, kernel_size=(1, n))
            j = np.argmin(mean_values[:, n_2])
            mean_value = mean_values[j, n_2]
            location = mac_map[mac][j]

            if mac in mac_mean_value:  # filled by slave!
                mean_value_slave = mac_mean_value[mac]
                if mean_value_slave > mean_value:
                    mac_mean_value[mac] = mean_value
                    mac_location[mac] = location
            else:
                mac_mean_value[mac] = mean_value
                mac_location[mac] = location

        except:
            pass

        # !!!INJECTION!!!
        # Keep only one tracker from heap. Store only minimal value of distance!
        # mac_map_new = copy.deepcopy(mac_map)
    test_array = np.zeros((40, n))
    for mac in mac_map:
        try:
            sql_query_minimal = "SELECT * FROM TrackerNames WHERE mac=%s;"
            c.execute(sql_query_minimal, mac)
            listed_result = list(c.fetchall())[0]  # mac is unique!
            if listed_result[4] != ' ':  # is slave tracker

                # slave data
                mac_slave = mac
                location_slave = mac_location[mac_slave]
                mean_value_slave = mac_mean_value[mac_slave]

                # get master for current slave
                name_master = listed_result[4]
                sql_master_query = "SELECT mac FROM TrackerNames WHERE name=%s;"
                c.execute(sql_master_query, name_master)
                listed_mac = list(c.fetchall())
                mac_master = listed_mac[0][0]

                # get master data
                # location_master = mac_location[mac_master] -- station name
                if mac_master in mac_mean_value:
                    mean_value_master = mac_mean_value[mac_master]
                    if mean_value_slave < mean_value_master:
                        mac_mean_value[mac_master] = mean_value_slave
                        mac_location[mac_master] = location_slave
                else:
                    mac_mean_value[mac_master] = mean_value_slave
                    mac_location[mac_master] = location_slave
                print()
                # update master
                # mac_location[mac_master] = location_slave if (location_slave < location_master) else location_master
                # mac_location.pop(mac_slave, None)
                # mac_mean_value[mac_master] = mean_value_slave if (mean_value_slave < mean_value_master) else mean_value_master
                # mac_mean_value.pop(mac_slave, None)

                # remove slave
                # mac_map_new.pop(mac_slave, None)
                # mac_map.pop(mac_slave, None)

                continue  # no work for slave
        except:
            pass
        # !!!END OF INJECTION!!!

        # Here are only MASTER trackers!!! Not any slave!
    for mac in mac_map:
        # print(mac)
        try:
            location = mac_location[mac]
            mean_value = mac_mean_value[mac]

            if triangulate:  # trilateration!
                location_first = location
                mean_value_first = mean_value

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
                        index_dist = mac_map[mac].index(loc)
                        if value_array[index_dist, -1] == MISC_VALUE:
                            continue
                        indexs_locs.append(i)
                        indexs_dist.append(index_dist)
                    except:
                        pass

                if not indexs_locs:
                    continue

                dist_select = mean_values[indexs_dist, n_2]
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

            bmb_check = "SELECT * FROM ignorePlayerList WHERE mac = %s;"
            # TODO: check location/mac
            # c.execute(bmb_check, mac)
            c.execute(bmb_check, location)
            row_count = c.rowcount
            if row_count == 0:
                insert_location_sql = "INSERT INTO playerLocation (mac, location, bleSignal) " \
                                      "VALUES (%s,%s,%s) ON DUPLICATE KEY " \
                                      "UPDATE mac = %s, location = %s, bleSignal = %s";
                c.execute(insert_location_sql, (mac, location, mean_value_str,
                                                mac, location, mean_value_str))
        except:
            pass
    delta_time = datetime.now() - timedelta(minutes=1)
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
