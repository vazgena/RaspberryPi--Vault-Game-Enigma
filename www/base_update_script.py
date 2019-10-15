
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
        set_str = ', '.join(['{0}={1}'.format(field, value if not isinstance(value, str) else "'{}'".format(value))
                             for field, value in zip(fixe[2], fixe[3])])
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
         ["Launch a Fake Blast. It won\\'t hurt them, but it will scare them!", 1, "2", 'no']),
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


def update_15_07_2019():
    connection = data_connect()
    con = connection.cursor()

    # fixed =[(table, id, fields, values)]
    fixes = [
        ('market', 29, ('selectable',), ('no',)),
        ('market', 13, ('text',), ('Detonate all blasts you have previously deployed in 10 seconds.',)),
        ('market', 15, ('cost',), (1,)),
        ('market', 18, ('cost', 'multipleAllowed'), (1, 1)),
        ('market', 21, ('multipleAllowed', 'cost'), ('2', 1)),
        ('market', 22, ('multipleAllowed',), (2,)),
        ('market', 24, ('multipleAllowed',), (1,)),
        ('market', 25, ('multipleAllowed',), (2,)),
    ]

    update_rows(con, fixes)
    connection.close()


def update_17_07_2019():
    connection = data_connect()
    con = connection.cursor()

    fixes = [
        ('cameraLocations', 7, ('ip',), ('http://10.255.1.249:8081/',))
    ]

    update_rows(con, fixes)
    connection.close()


def add_incoming_bomb():
    connection = data_connect()
    con = connection.cursor()
    query = "ALTER TABLE bombsDeployed ADD timeIncoming datetime DEFAULT NULL"
    con.execute(query)
    connection.close()


def update_22_07_2019():
    connection = data_connect()
    con = connection.cursor()

    fixes = [
        ('stationList', 7, ('nameSpelled', 'hint_text'), ('DEFENSE', "You can select a station and check if there\\'s a blast layed")),
        ('stationList', 16, ('nameSpelled', 'hint_text'), ('DEFENSE', "You can select a station and check if there\\'s a blast layed"))
    ]

    update_rows(con, fixes)
    connection.close()


def create_table_volume():
    connection = data_connect()
    con = connection.cursor()

    sql_command = """
CREATE TABLE `station_volume` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `station` varchar(100) NOT NULL,
  `volume` float(53) NOT NULL,
  `id_volume_tag` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `station` (`station`)
);
    """
    con.execute(sql_command)
    connection.close()


def update_24_07_2019():
    connection = data_connect()
    con = connection.cursor()

    insertes = [
        ('station_volume', ['station', 'volume', 'id_volume_tag'],
         ["MAN1", 0.7, 'volume_labyrinth']),
        ('station_volume', ['station', 'volume', 'id_volume_tag'],
         ["MAN2", 0.7, 'volume_enigma']),
    ]
    insert_rows(con, insertes)
    connection.close()

def add_column_station():
    connection = data_connect()
    con = connection.cursor()

    query = "ALTER TABLE stationList " \
            "ADD COLUMN lay_bomb BOOLEAN NOT NULL DEFAULT TRUE"
    con.execute(query)
    connection.close()


def update_11_10_2019():
    connection = data_connect()
    con = connection.cursor()

    #  oh 1 small change - can we remove the blast station as an option for the Charge and Steal station - meaning
    #  stations charge and steal no longer have the blast (middle) station as an option the light can't light up there
    #  anyway so it can't be there
    query = "ALTER TABLE stationList " \
            "ADD COLUMN is_visible BOOLEAN NOT NULL DEFAULT TRUE"
    con.execute(query)

    fixes = [
        ('stationList', 14, ('is_visible',), (False,)),
        ('stationList', 5, ('is_visible',), (False,))
    ]
    update_rows(con, fixes)

    # trackers heap fixes
    query = "ALTER TABLE TrackerNames " \
            "ADD COLUMN created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, " \
            "ADD COLUMN master_name varchar(4) DEFAULT '', " \
            "ADD COLUMN angle_clockwise int(11) DEFAULT '0'"
    con.execute(query)

    connection.close()


def update_24_07_2019_2():
    connection = data_connect()
    con = connection.cursor()

    fixes = [
        ('stationList', 5, ('lay_bomb',),
         (False,)),
        ('stationList', 14, ('lay_bomb',),
         (False,))
    ]

    update_rows(con, fixes)
    connection.close()


def create_table_defence():
    connection = data_connect()
    con = connection.cursor()

    sql_command = """
    CREATE TABLE `station_defence` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `station` varchar(100) NOT NULL,
      `room` int(11) NOT NULL,
      `status` varchar(100) NOT NULL,
      `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      UNIQUE KEY `station` (`station`)
    );
        """
    con.execute(sql_command)
    connection.close()

def init_log_table():
    connection = data_connect()
    con = connection.cursor()

    sql_command = """
            CREATE TABLE `trackers_value` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `mac` varchar(255) NOT NULL,
              `station` varchar(100) NOT NULL,
              `value` float(53) NOT NULL,
              `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`)
            );
                """
    con.execute(sql_command)
    connection.close()

def update_icon_defense():
    connection = data_connect()
    con = connection.cursor()

    fixes = [
        ('stationList', 7, ('image',),
         ("18_EV_Detect_Button_FINAL_v2.png",)),
        ('stationList', 16, ('image',),
         ("18_EV_Detect_Button_FINAL_v2.png",))
    ]

    update_rows(con, fixes)
    connection.close()


def init_table_position():
    connection = data_connect()
    con = connection.cursor()

    sql_command = """
            CREATE TABLE `station_position` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `room` int(11) NOT NULL,
              `station` varchar(100) NOT NULL,
              `x` float(53) NOT NULL,
              `y` float(53) NOT NULL,
              PRIMARY KEY (`id`)
            );
                """
    con.execute(sql_command)
    connection.close()


def add_position():
    connection = data_connect()
    con = connection.cursor()
    # insertes =[(table, fields, values)]
    insertes = [
        ('station_position', ['room', 'station', 'x', 'y'],
         [1, 'MKP1', 0, 8]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [1, 'MOR1', 7, 15.3]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [1, 'MTR1', 13, 15.3]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [1, 'CS11', 19, 15.3]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [1, 'MAN1', 6.4, 0]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [1, 'MAS1', 13, 0]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [1, 'AUD1', 19, 0]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [1, 'HAC1', 25, 7.2]),
    ]
    insert_rows(con, insertes)

    insertes = [
        ('station_position', ['room', 'station', 'x', 'y'],
         [2, 'MKP2', 0, 7]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [2, 'MOR2', 6.6, 13]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [2, 'MTR2', 13.2, 13]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [2, 'CS12', 20.2, 13]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [2, 'MAN2', 7, 0]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [2, 'MAS2', 14.3, 0]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [2, 'AUD2', 21.3, 0]),
        ('station_position', ['room', 'station', 'x', 'y'],
         [2, 'HAC2', 25.8, 6.2]),
    ]
    insert_rows(con, insertes)

    connection.close()


def create_calibration_table():
    connection = data_connect()
    con = connection.cursor()

    sql_command = """
                CREATE TABLE `tracker_calibration` (
                  `id` int(11) NOT NULL AUTO_INCREMENT,
                  `mac` varchar(255) NOT NULL,
                  `station` varchar(100) NOT NULL,
                  `tx_power` float(53) NOT NULL,
                  PRIMARY KEY (`id`)
                );
                    """
    con.execute(sql_command)
    connection.close()


def create_temp_calibration_table():
    connection = data_connect()
    con = connection.cursor()

    sql_command = """
                   CREATE TABLE `temp_calibration` (
                     `id` int(11) NOT NULL AUTO_INCREMENT,
                     `mac` varchar(255) NOT NULL,
                     `station` varchar(100) NOT NULL,
                     `tx_power` float(53) NOT NULL,
                     `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                     PRIMARY KEY (`id`)
                   );
                       """
    con.execute(sql_command)
    connection.close()


def create_table_distance():
    connection = data_connect()
    con = connection.cursor()

    sql_command = """
    CREATE TABLE `distance_value` (
                     `id` int(11) NOT NULL AUTO_INCREMENT,
                     `mac` varchar(255) NOT NULL,
                     `station` varchar(100) NOT NULL,
                     `tx_power` float(53) NOT NULL,
                     `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                     `distance` float(53) NOT NULL,
                     PRIMARY KEY (`id`)
                   );
    
    """

    con.execute(sql_command)
    connection.close()


def create_table_coef():
    connection = data_connect()
    con = connection.cursor()

    sql_command = """
    CREATE TABLE `coefficient` (
                     `id` int(11) NOT NULL AUTO_INCREMENT,
                     `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                     `a` float(53) NOT NULL,
                     `b` float(53) NOT NULL,
                     `c` float(53) NOT NULL,
                     PRIMARY KEY (`id`)
                   );

    """

    con.execute(sql_command)
    connection.close()



if __name__ == "__main__":

    # update_09_07_2019()
    # check_market_table()
    # add_color_market()
    # update_12_07_2019()
    # add_fake_bomb()
    # update_15_07_2019()
    # update_17_07_2019()
    # add_incoming_bomb()
    # update_22_07_2019()
    # create_table_volume()
    # update_24_07_2019()
    # add_column_station()
    # update_24_07_2019_2()
    # create_table_defence()
    # init_log_table()
    # update_icon_defense()
    # init_table_position()
    # add_position()
    # create_calibration_table()
    # create_temp_calibration_table()
    # create_table_distance()
    # create_table_coef()
    update_11_10_2019()
    pass

