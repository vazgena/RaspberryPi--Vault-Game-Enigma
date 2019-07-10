
from time import sleep
from pymysql import InternalError, connect


dbuser = 'game'
dbpass = 'h95d3T7SXFta'


def data_connect():
    return connect(
        db='game',
        user=dbuser,
        passwd=dbpass,
        host='localhost',
        autocommit=True)


sleep(20)
connection = data_connect()
c = connection.cursor()
try:
    reset_trackers = "TRUNCATE TABLE playerLocation"
    c.execute(reset_trackers)
except InternalError:
    pass
connection.close()
print("trackers reset")
sleep(5)
