

import re
import json
from datetime import datetime
from pymysql import InternalError, connect

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


def init_log_table():
    connection = data_connect()
    con = connection.cursor()

    sql_command = """
        CREATE TABLE `log_tracker` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `mac` varchar(255) NOT NULL,
          `station` varchar(100) NOT NULL,
          `room` int(11) NOT NULL,
          `volume` float(53) NOT NULL,
          `timestamp` DATETIME NOT NULL,
          PRIMARY KEY (`id`)
        );
            """
    con.execute(sql_command)
    connection.close()


def insert_rows(conn, insertes):
    # insertes =[(table, fields, values)]
    insert_request_template = "INSERT INTO {0} ({1}) VALUES ({2});"
    for inserte in insertes:
        value_row = ', '.join([str(val) if not isinstance(val, (str, datetime)) else "'{}'".format(val) for val in inserte[2]])
        command_str = insert_request_template.format(inserte[0], ', '.join(inserte[1]), value_row)
        conn.execute(command_str)


def parse_log(line):
    if not "ImmutableMultiDict" in line:
        return None
    split_line = line.split(' - ')
    date = datetime.strptime(split_line[0], "%Y-%m-%d %H:%M:%S,%f")
    data_str = split_line[-1][19: -2]
    data_str = data_str.replace('(', '[')
    data_str = data_str.replace(')', ']')
    data_str = data_str.replace('\'', '"')
    data = json.loads(data_str)
    data_dict = dict(data)
    data_dict['timestamp'] = date
    data_dict['avg'] = float(data_dict['avg'])

    return data_dict
    a = 1


def read_log(file_name):
    connection = data_connect()
    con = connection.cursor()
    i = 0
    with open(file_name, 'r') as f:
        for line in f:
            data_dict = parse_log(line)
            if data_dict:
                insert_rows(con, [('log_tracker', ('mac', 'station', 'room', 'volume', 'timestamp'),
                                (data_dict['bt_addr'], data_dict['station'], data_dict['room'], data_dict['avg'], data_dict['timestamp'])),])
                i += 1
                print(i)

    connection.close()


if __name__ == "__main__":
    init_log_table()
    read_log("track1.log")
