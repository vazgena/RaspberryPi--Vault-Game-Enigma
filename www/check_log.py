

import os
import re
import json
from datetime import datetime
from pymysql import InternalError, connect
import asyncio
import concurrent.futures

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


def reverse_readline(filename, buf_size=8192):
    """A generator that returns the lines of a file in reverse order"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # The first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # If the previous chunk starts right from the beginning of line
                # do not concat the segment to the last line of new chunk.
                # Instead, yield the segment first
                if buffer[-1] != '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if lines[index]:
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment



def insert_rows(conn, insertes):
    # insertes =[(table, fields, values)]
    insert_request_template = "INSERT INTO {0} ({1}) VALUES ({2});"
    for inserte in insertes:
        value_row = ', '.join([str(val) if not isinstance(val, (str, datetime)) else "'{}'".format(val) for val in inserte[2]])
        command_str = insert_request_template.format(inserte[0], ', '.join(inserte[1]), value_row)
        conn.execute(command_str)


# n = 1758350
n = 571770

def parse_log(line):
    if not "ImmutableMultiDict" in line:
        return None
    split_line = line.split(' - ')
    date = datetime.strptime(split_line[0], "%Y-%m-%d %H:%M:%S,%f")
    data_str = split_line[-1][19: -1]
    data_str = data_str.replace('(', '[')
    data_str = data_str.replace(')', ']')
    data_str = data_str.replace('\'', '"')
    data_str = data_str.replace('"{', '{')
    data_str = data_str.replace('}"', '}')
    try:
        data = json.loads(data_str)
        data_dict = dict(data)
        data_dict['timestamp'] = date
        data_dict['avg'] = float(data_dict['avg'])
        return data_dict
    except BaseException as e:
        print(data_str)
        raise


def process_line(line):
    data_dict = parse_log(line)
    if data_dict['timestamp'] < datetime.strptime("2019-07-26 10:00:00,000", "%Y-%m-%d %H:%M:%S,%f"):
        return

    connection = data_connect()
    con = connection.cursor()
    insert_rows(con, [('log_tracker', ('mac', 'station', 'room', 'volume', 'timestamp'),
                       (data_dict['bt_addr'], data_dict['station'], data_dict['room'], data_dict['avg'],
                        data_dict['timestamp'])), ])

    connection.close()



async def read_log(file_name, n_task=100):
    connection = data_connect()
    con = connection.cursor()
    i = -1
    loop = asyncio.get_event_loop()
    tasks = []
    # with open(file_name, 'r') as f:
    #     for line in f:
    #         i += 1
    #         if i < n:
    #             continue
    #         task = loop.run_in_executor(None, process_line, line)
    #         tasks.append(task)
    #
    #         if len(tasks) < n_task:
    #             continue
    #         done, tasks = await asyncio.wait(tasks, return_when=concurrent.futures.FIRST_COMPLETED)
    #         tasks = list(tasks)
    #         print(i)

    for line in reverse_readline(file_name):
            task = loop.run_in_executor(None, process_line, line)
            tasks.append(task)

            if len(tasks) < n_task:
                continue
            done, tasks = await asyncio.wait(tasks, return_when=concurrent.futures.FIRST_COMPLETED)
            tasks = list(tasks)
            print(i)
    if len(tasks) > 0:
        _, _ = await asyncio.wait(tasks, return_when=concurrent.futures.ALL_COMPLETED)

    connection.close()


if __name__ == "__main__":
    # init_log_table()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_log("track.log"))
