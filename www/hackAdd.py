from time import sleep
from pymysql import connect


db_user = 'game'
db_pass = 'h95d3T7SXFta'


def data_connect():
    return connect(
        db='game',
        user=db_user,
        passwd=db_pass,
        host='localhost',
        autocommit=True)


def hack_add():
    timer = 60
    connection = data_connect()
    c = connection.cursor()
    hack_rate_time_sql = "SELECT * FROM hackrate"
    c.execute(hack_rate_time_sql)
    hack_rate_time_list = list(c.fetchall())
    for i in hack_rate_time_list:
        timer = i[1]
        rate = i[2]
    sleep(timer)
    timed_hack_add = "SELECT * FROM hacks WHERE team = '1';"
    c.execute(timed_hack_add)
    current_hack_sql = list(c.fetchall())
    for i in current_hack_sql:
        funding1 = "INSERT INTO hacks (team, howMany) VALUES ('1', %s) ON DUPLICATE KEY UPDATE" \
                   " team = '1', howMany = %s;"
        c.execute(funding1, (int(i[2]) + int(rate), int(i[2]) + int(rate)))
    timed_hack_add_2 = "SELECT * FROM hacks WHERE team = '2';"
    c.execute(timed_hack_add_2)
    current_hack_sql = list(c.fetchall())
    for i in current_hack_sql:
        funding_2 = "INSERT INTO hacks (team, howMany) VALUES ('2', %s) ON DUPLICATE KEY UPDATE"\
                    " team = '2', howMany = %s;"
        c.execute(funding_2, (int(i[2]) + int(rate), int(i[2]) + int(rate)))
    connection.close()


while True:
    hack_add()
