# import os, ssl, sys, time, atexit, collections
from time import sleep
from random import randrange, choice
from pymysql import InternalError, connect


# Variables
dbuser = 'game'
dbpass = 'h95d3T7SXFta'
dbhost = 'localhost'
colors = ["red", "green", "blue", "yellow"]
colors2 = ["red", "green", "blue", "yellow"]
start_again = True
station_list_1 = ["CS11", "CS21", "AUD1", "HAC1", "MKP1", "MAS1", "MTR1", "MOR1"]
station_list_2 = ["CS12", "CS22", "AUD2", "HAC2", "MKP2", "MAS2", "MTR2", "MOR2"]
on = "on"
off = "off"
room1 = "1"
room2 = "2"


def dataconnect():
	return connect(
		db=dbuser,
		user=dbuser,
		passwd=dbpass,
		host=dbhost,
		autocommit=True)


def runonce():
	connection = dataconnect()
	c = connection.cursor()
	clear_current_color_sql = "TRUNCATE TABLE currentColor"
	c.execute(clear_current_color_sql)
	connection.close()
	loop()


def loop():
	timer = randrange(15, 75)
	sleep(timer)
	while True:

		connection = dataconnect()
		c = connection.cursor()
		clear_current_color_sql = "TRUNCATE TABLE currentColor"
		sleep(2)
		c.execute(clear_current_color_sql)
		timer_color = choice(colors)
		timer_color2 = choice(colors2)
		rooms1selected = choice(station_list_1)
		rooms2selected = choice(station_list_2)
		incert_color1 = "INSERT INTO currentColor (station, color, lightON, room) VALUES (%s, %s, %s, %s);"
		c.execute(incert_color1, (rooms1selected, timer_color, on, room1))
		incert_color2 = "INSERT INTO currentColor (station, color, lightON, room) VALUES (%s, %s, %s, %s);"
		c.execute(incert_color2, (rooms2selected, timer_color2, on, room2))
		while not start_again:
			sleep(1)
		sleep_timer = randrange(15, 75)
		slept = 0
		while slept < sleep_timer:
			slept = slept + 3
			sleep(3)
			try:
				light_off = "UPDATE currentColor SET lightON  = %s WHERE station = %s;"
				c.execute(light_off, (off, rooms1selected))
			except InternalError:
				pass
			try:
				light_off = "UPDATE currentColor SET lightON  = %s WHERE station = %s;"
				c.execute(light_off, (off, rooms2selected))
			except InternalError:
				pass
			timers = randrange(4, 8)
			slept = slept + timers
			sleep(timers)
			try:
				light_on = "UPDATE currentColor SET lightON  = %s WHERE station = %s;"
				c.execute(light_on, (on, rooms1selected))
			except InternalError:
				pass
			try:
				light_on = "UPDATE currentColor SET lightON  = %s WHERE station = %s;"
				c.execute(light_on, (on, rooms2selected))
			except InternalError:
				pass
		try:
			light_off = "UPDATE currentColor SET lightON  = %s WHERE station = %s;"
			c.execute(light_off, (off, rooms1selected))
		except InternalError:
			pass
		try:
			light_off = "UPDATE currentColor SET lightON  = %s WHERE station = %s;"
			c.execute(light_off, (off, rooms2selected))
		except InternalError:
			pass
		connection.close()


runonce()
