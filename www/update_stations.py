import os
from time import sleep
from pymysql import connect
from datetime import datetime, timedelta


# variables
dbuser = 'game'
dbpass = 'h95d3T7SXFta'
station_name = ""
room = "1"
jobs = []


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# NAME_SCRIPT = ["playerTracking.py", "ipadress.py", 'color_local.py', 'startup.py']
NAME_SCRIPT = ["playerTracking.py"]


# database connection
def dataconnect():
    return connect(db='game', user=dbuser, passwd=dbpass, host='localhost', autocommit=True)


def get_station_ip():
    sql_request = "SELECT station_ips.ipaddress FROM stationList LEFT JOIN station_ips ON stationList.name = station_ips.station;"
    connection = dataconnect()
    c = connection.cursor()
    c.execute(sql_request)
    station_rows = list(c.fetchall())
    connection.close()
    for station_row in station_rows:
        station_ip = station_row[0]
        yield station_ip


def scp_update_file(file_name, ip, password='1qaz2wsx', read_folder=BASE_DIR, result_folder='~'):
    scp_command = "sshpass -p '{0}' scp {1} pi@{2}:{3}"
    file_path = os.path.join(read_folder, file_name)
    execute_command = scp_command.format(password, file_path, ip, result_folder)
    os.system(execute_command)


def main():
    ip_list = list(get_station_ip())
    ip_list = ['192.168.2.200']
    for file_name in NAME_SCRIPT:
        for ip in ip_list:
            try:
                scp_update_file(file_name, ip, 'raspberry')
                # scp_update_file(file_name, ip)
            except BaseException as e:
                print(e)


if __name__ == "__main__":
    main()
