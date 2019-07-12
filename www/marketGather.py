from pymysql import connect
from time import sleep
from random import randint

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


def marketreplaceselect():
    connection = dataconnect()
    c = connection.cursor()
    numberOwnedTotal = 0
    marketText = ""
    marketCost = ""
    marketMultiple = ""
    isDifferent = False

    while isDifferent == False:
        marketAvailableListed = []
        getTableListSQL = 'SELECT * FROM market ORDER BY RAND() LIMIT 1;'
        c.execute(getTableListSQL)
        marketAvailableList = list(c.fetchall())
        for i in marketAvailableList:
            isTheSameCheck = 'SELECT * FROM marketCurrent WHERE text = %s'
            c.execute(isTheSameCheck, i[1])
            rowCount = c.rowcount
            if rowCount == 0:
                getQuantAvail = "SELECT * FROM marketOwned WHERE itemID = %s"
                c.execute(getQuantAvail, i[0])
                counted = c.rowcount
                if counted == 0:
                    isDifferent = True
                else:
                    checkQuantityOwned = list(c.fetchall())
                    for j in checkQuantityOwned:
                        numberOwnedTotal = numberOwnedTotal + int(j[2])
                    if (numberOwnedTotal < int(i[3])):
                        isDifferent = True
            else:
                pass

    for i in marketAvailableList:
        marketText = i[1]
        marketCost = i[2]
        marketMultiple = i[3]
        marketID = i[0]
        marketIncertSQL = 'INSERT INTO marketCurrent (text, cost, itemID, multipleAllowed) VALUES (%s, %s, %s, %s);'
        c.execute(marketIncertSQL, (marketText, marketCost, marketID, marketMultiple))
    connection.close()





def runOnce():
    connection = dataconnect()
    c = connection.cursor()
    marketAvailableListed = []
    getTableListSQL = 'SELECT * FROM market ORDER BY RAND() LIMIT 3;'
    c.execute(getTableListSQL)
    marketAvailableList = list(c.fetchall())
    clearMarketSQL = 'TRUNCATE TABLE marketCurrent;'
    c.execute(clearMarketSQL)
    for i in marketAvailableList:
        marketText = i[1]
        marketCost = i[2]
        marketMultiple = i[3]
        marketID = i[0]
        marketIncertSQL = 'INSERT INTO marketCurrent (text, cost, itemID, multipleAllowed) VALUES (%s, %s, %s, %s);'
        c.execute(marketIncertSQL, (marketText, marketCost, marketID, marketMultiple))
    connection.close()


def gameStart():
    runOnce()
    global running
    running = True
    timer_count = 0
    while running == True:
        connection = dataconnect()
        c = connection.cursor()
        # sleep_timer = 10
        sleep_timer = randint(30, 50)
        while timer_count <= sleep_timer:
            sleep(1)
            check_bought_sql = "SELECT * FROM marketCurrent WHERE purchased = %s"
            c.execute(check_bought_sql, "Yes")
            rowcount = c.rowcount
            if rowcount != 0:
                delete_market = "DELETE FROM marketCurrent WHERE purchased = %s LIMIT 1"
                c.execute(delete_market, "Yes")
                marketreplaceselect()
                timer_count = 0
            timer_count = timer_count + 1

        clearMarketSQL = 'DELETE FROM marketCurrent ORDER BY id ASC LIMIT 1;'
        c.execute(clearMarketSQL)
        marketreplaceselect()
        timer_count = 0


gameStart()