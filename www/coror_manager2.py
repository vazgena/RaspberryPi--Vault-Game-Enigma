# import os, ssl, sys, time, atexit, collections
from time import sleep
from random import randrange, choice
from pymysql import InternalError, connect


# Variables
dbuser = 'game'
dbpass = 'h95d3T7SXFta'
dbhost = 'localhost'

colors = ["red", "green", "blue"]
start_again = True
station_list = []
on = "on"
off = "off"
room = "2"
no = "No"
yes = "Yes"


def dataconnect():
	return connect(
		db=dbuser,
		user=dbuser,
		passwd=dbpass,
		host=dbhost,
		autocommit=True)


def run_once():
	# Open database connection
	connection = dataconnect()
	c = connection.cursor()

	# Clear all from color table.
	clear_current_color_sql = "TRUNCATE TABLE currentColor"
	c.execute(clear_current_color_sql)

	# Get list from stations table.
	station_list_sql = 'SELECT * FROM stationList WHERE room = %s'
	c.execute(station_list_sql, room)
	station_listed = list(c.fetchall())
	for i in station_listed:
		name = i[1]
		if name != "BMB2":
			station_list.append(name)
		else:
			pass

	# Close the connection and start the loop.
	connection.close()
	loop()


def loop():
	while True:
		# Open database connection
		connection = dataconnect()
		c = connection.cursor()

		# check if there is a color entered in the table already. If not add one.
		check_for_sql = "SELECT * FROM currentColor WHERE room = %s"
		c.execute(check_for_sql, room)
		row_count = c.rowcount
		if row_count == 0:
			timer_color = choice(colors)
			rooms_selected = choice(station_list)
			insert_color = "INSERT INTO currentColor (station, color, lightON, room) VALUES (%s, %s, %s, %s);"
			c.execute(insert_color, (rooms_selected, timer_color, on, room))
		else:
			pass

		# check if the mine has been mined
		get_color_mined_sql = "SELECT * FROM currentColor WHERE collected = %s"
		c.execute(get_color_mined_sql, yes)
		row_count = c.rowcount
		if row_count != 0:
			sleep(randrange(10, 20))
			delete_color = "DELETE FROM currentColor WHERE room = %s"
			c.execute(delete_color, room)
			timer_color = choice(colors)
			rooms_selected = choice(station_list)
			insert_color = "INSERT INTO currentColor (station, color, lightON, room) VALUES (%s, %s, %s, %s);"
			c.execute(insert_color, (rooms_selected, timer_color, on, room))
			timer_color = choice(colors)
			rooms_selected = choice(station_list)
			if c.rowcount == 0:
				insert_color = "INSERT INTO currentColor (station, color, lightON, room) VALUES (%s, %s, %s, %s);"
				c.execute(insert_color, (rooms_selected, timer_color, on, room))

		light_off = "UPDATE currentColor SET lightON  = %s WHERE room = %s;"
		c.execute(light_off, (on, room))
		sleep(3)
		light_off = "UPDATE currentColor SET lightON  = %s WHERE room = %s;"
		c.execute(light_off, (off, room))
		timers = randrange(4, 8)
		sleep(timers)



		sleep(1)
		connection.close()


run_once()