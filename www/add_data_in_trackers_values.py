import datetime
import time
from pymysql import InternalError, connect
from pyinstrument import Profiler

dbuser = 'game'
dbpass = 'h95d3T7SXFta'


# databace connection
def dataconnect():
    return connect(
        db='game',
        user=dbuser,
        passwd=dbpass,
        host='localhost',
        autocommit=True)


# adding data from trackers_value2 to trackers_value every second
def adding_data(num_second, num_minute, c):
    get_new_locations = "SELECT * from game.trackers_value2 where timestamp = '2019-10-18 02:{1}:{0}';".format(
        num_second, num_minute)
    c.execute(get_new_locations)
    list_data = list(c.fetchall())
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for data in list_data:
        if data[1] == "ec:fe:7e:00:03:9f" or data[1] == "ec:fe:7e:10:92:73":
            macstat = str(data[1]) + " " + str(data[2])
            room = int(data[2][-1])
            add_data_in_trackers = "INSERT INTO trackers (macstat, mac, station, signal_avg, room) " \
                                   "VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
                                   "macstat = %s, mac = %s, station = %s, signal_avg = %s, room = %s, timestamp = %s"

            add_data_in_tracker_value = "INSERT INTO trackers_value (id, mac, station, value, timestamp) " \
                                        "VALUES({0}, '{1}', '{2}', {3}, '{4}');".format(data[0], data[1], data[2],
                                                                                        data[3],
                                                                                        now)
            c.execute(add_data_in_trackers, (macstat, data[1], data[2], data[3], room, macstat,
                                   data[1], data[2], data[3], room, now))

            c.execute(add_data_in_tracker_value)
    time.sleep(0.8)


if __name__ == "__main__":
    connection = dataconnect()
    c = connection.cursor()
    num_second = 33
    num_minute = 21
    while True:
        if num_second == 60:
            num_second = 0
            num_minute = num_minute + 1
        adding_data(num_second, num_minute, c)
        num_second = num_second + 1

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
