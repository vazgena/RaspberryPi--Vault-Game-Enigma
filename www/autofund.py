from time import sleep
from pymysql import connect


dbuser = 'game'
dbpass = 'h95d3T7SXFta'


def dataconnect():
    return connect(
        db='game',
        user=dbuser,
        passwd=dbpass,
        host='localhost',
        autocommit=True)


def fundsloop():
    timer = 45
    connection = dataconnect()
    c = connection.cursor()
    timedb = 'SELECT * FROM timer; '
    c.execute(timedb)
    timedblist = list(c.fetchall())
    for i in timedblist:
        timer = i[1]
    sleep(timer)
    currerntfunds1 = "SELECT * FROM currency WHERE room = %s;"
    c.execute(currerntfunds1, "1")
    currerntfundsnum1 = list(c.fetchall())

    for i in currerntfundsnum1:
        funds1 = int(i[1])+1
        addfunds1 = "INSERT INTO currency (room, amount) VALUES ('1', %s) " \
                    "ON DUPLICATE KEY UPDATE room = '1', amount = %s;"
        c.execute(addfunds1, (int(funds1), int(funds1)))

    currerntfunds2 = "SELECT * FROM currency  WHERE room = %s;"
    c.execute(currerntfunds2, "2")
    currerntfundsnum2 = list(c.fetchall())

    for i in currerntfundsnum2:
        funds2 = int(i[1])+1
        addfunds2 = "INSERT INTO currency (room, amount) VALUES ('2', %s) " \
                    "ON DUPLICATE KEY UPDATE room = '2', amount = %s;"
        c.execute(addfunds2, (int(funds2), int(funds2)))
        connection.close()
        

while True:
    fundsloop()
