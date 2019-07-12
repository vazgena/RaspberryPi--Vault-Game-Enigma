
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



def update_rows(conn, fixes):
    # fixed =[(table, id, fields, values)]
    update_request_template = "UPDATE {0} SET {1} WHERE id={2};"
    for fixe in fixes:
        set_str = ', '.join(['{0}={1}'.format(field, value) for field, value in zip(fixe[2], fixe[3])])
        command_str = update_request_template.format(fixe[0], set_str, fixe[1])
        conn.execute(command_str)


def remove_rows(conn, removes):
    remove_request_template = "DELETE FROM {0} WHERE id={1};"
    for remove in removes:
        command_str = remove_request_template.format(*remove)
        conn.execute(command_str)


def insert_rows(conn, insertes):
    # insertes =[(table, fields, values)]
    insert_request_template = "INSERT INTO {0} ({1}) VALUES ({2});"
    for inserte in insertes:
        value_row = ', '.join([str(val) if not isinstance(val, str) else "'{}'".format(val) for val in inserte[2]])
        command_str = insert_request_template.format(inserte[0], ', '.join(inserte[1]), value_row)
        conn.execute(command_str)


def update_09_07_2019():
    connection = data_connect()
    con = connection.cursor()

    # fixed =[(table, id, fields, values)]
    fixes = [
        ('market', 9, ('cost',), (4,)),
        ('market', 10, ('cost',), (6,)),
        ('market', 12, ('cost', 'text'), (4, "See the positions of all of your opponent\\'s blasts.")),
        ('market', 13, ('text', ), ('Detonate all blasts you have previously deployed 10 in 10 seconds.', )),
        ('market', 15, ('cost',), (1,)),
        ('market', 18, ('multipleAllowed', 'cost'), ('1', 1)),
        ('market', 21, ('multipleAllowed', 'cost'), ('1', 2)),
        ('market', 22, ('multipleAllowed', 'cost'), ('2', 1)),
        ('market', 24, ('multipleAllowed',), ('1',)),
        ('market', 25, ('multipleAllowed',), ('2',)),
    ]
    update_rows(con, fixes)

    # removes =[(table, id)]
    removes = [
        ('market', 1),
        ('market', 2),
        ('market', 6)
    ]
    remove_rows(con, removes)

    # # insertes =[(table, fields, values)]
    # insertes = [
    #     ('market', ['text', 'cost', 'multipleAllowed'],
    #      ["Launch a Fake Blast. It won\\'t hurt them, but it will scare them!", 1, "2"]),
    #     ('market', ['text', 'cost', 'multipleAllowed'],
    #      ['3 Stations get hacked at random.', 4, "1"])
    # ]
    # insert_rows(con, insertes)

    connection.close()


def update_12_07_2019():
    connection = data_connect()
    con = connection.cursor()
    # insertes =[(table, fields, values)]
    insertes = [
        ('market', ['text', 'cost', 'multipleAllowed', 'selectable'],
         ["Launch a Fake Blast. It won\\'t hurt them, but it will scare them!", 1, "2", 'yes']),
        ('market', ['text', 'cost', 'multipleAllowed', 'selectable'],
         ['3 Stations get hacked at random.', 4, "1", 'no'])
    ]
    insert_rows(con, insertes)

    connection.close()



def check_market_table():
    command = "SELECT * from market;"
    connection = data_connect()
    conn = connection.cursor()
    conn.execute(command)
    response = list(conn.fetchall())
    for row in response:
        print(row)

    connection.close()


def add_color_market():
    connection = data_connect()
    con = connection.cursor()
    query = "ALTER TABLE stationList ADD color_selected_assist VARCHAR(250) NOT NULL DEFAULT ''"
    station_list = "SELECT * FROM stationList;"
    query_update = "UPDATE stationList SET color_selected_assist = %s WHERE id = %s ;"
    con.execute(query)
    con.execute(station_list)
    station_list_sql = list(con.fetchall())
    for i in station_list_sql:
        selected_color = i[15]
        id = i[0]
        selected_assist_color = selected_color.replace('320deg', '150deg')
        con.execute(query_update, (selected_assist_color, id))

    connection.close()


def add_fake_bomb():
    connection = data_connect()
    con = connection.cursor()
    query = "ALTER TABLE bombsDeployed ADD fake_bomb BOOLEAN NOT NULL DEFAULT FALSE"
    con.execute(query)
    connection.close()




if __name__ == "__main__":

    # update_09_07_2019()
    # check_market_table()
    # add_color_market()
    update_12_07_2019()
    add_fake_bomb()
