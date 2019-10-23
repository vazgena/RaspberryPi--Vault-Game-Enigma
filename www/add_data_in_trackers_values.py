import datetime
import time
from pymysql import InternalError, connect
# from pyinstrument import Profiler

dbuser = 'game'
dbpass = 'h95d3T7SXFta'


# databace connection
def dataconnect():
    return connect(
        db='game',
        user=dbuser,
        passwd=dbpass,
        host='localhost',
        autocommit=False)


# adding data from trackers_value2 to trackers_value every second
def adding_data(c, curent_time):
    get_new_locations = "SELECT * from game.trackers_value2 where timestamp = %s;"
    c.execute(get_new_locations, curent_time)
    list_data = list(c.fetchall())
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for data in list_data:
        if data[1] in ["ec:fe:7e:00:03:9f", "ec:fe:7e:10:92:73"]:
            macstat = str(data[1]) + " " + str(data[2])
            room = int(data[2][-1])
            add_data_in_trackers = "INSERT INTO trackers (macstat, mac, station, signal_avg, room) " \
                                   "VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
                                   "macstat = %s, mac = %s, station = %s, signal_avg = %s, room = %s, timestamp = %s"

            add_data_in_tracker_value = "INSERT INTO trackers_value (mac, station, value, timestamp) " \
                                        "VALUES('{0}', '{1}', {2}, '{3}');".format(data[1], data[2],
                                                                                        data[3],
                                                                                        now)
            c.execute(add_data_in_trackers, (macstat, data[1], data[2], data[3], room, macstat,
                                   data[1], data[2], data[3], room, now))

            c.execute(add_data_in_tracker_value)

def exsis_more(c, curent_time):
    get_new_locations = "SELECT COUNT(*) from game.trackers_value2 where timestamp > %s;"
    c.execute(get_new_locations, curent_time)
    list_data = list(c.fetchall())
    count = list_data[0][0]
    return count > 0


if __name__ == "__main__":
    connection = dataconnect()
    c = connection.cursor()
    start_time = datetime.datetime.strptime('2019-10-18 02:21:33', '%Y-%m-%d %H:%M:%S')
    curent_time = start_time
    while True:
        time_start = datetime.datetime.now()
        adding_data(c, curent_time)
        connection.commit()
        if not exsis_more(c, curent_time):
            break
        time_end = datetime.datetime.now()
        time_sleep = 1 - (time_end-time_start).seconds
        print(time_sleep)
        if time_sleep > 0:
            time.sleep(time_sleep)
        curent_time += datetime.timedelta(seconds=1)


# CREATE TABLE game.trackers
# (
# id int NOT NULL,
# macstat CHAR(60),
# mac CHAR(60),
# station CHAR(60),
# signal_avg float,
# room int,
# timestamp datetime,
# packet_data char(60),
# properties char(60),
# PRIMARY KEY (id)
# );
