# imports
from pymysql import connect
from time import sleep
from datetime import datetime, timedelta


# variables
dbuser = 'game'
dbpass = 'h95d3T7SXFta'
station_name = ""
room = "1"
jobs = []


# database connection
def dataconnect():
	return connect(
		db='game',
		user=dbuser,
		passwd=dbpass,
		host='localhost',
		autocommit=True)


def check_det():
	ttd = ""
	sleep(.5)
	global station_name
	do_not_check = []
	connection = dataconnect()
	c = connection.cursor()
	bmb_check = "SELECT * FROM bombsDeployed WHERE room = %s"
	c.execute(bmb_check, room)
	row_count = c.rowcount
	if row_count != 0:
		get_time_location = list(c.fetchall())
		do_not_check_sql = "SELECT * FROM ignoreList"
		c.execute(do_not_check_sql)
		row_count = c.rowcount
		if row_count != 0:
			do_not_check_list = list(c.fetchall())
			for m in do_not_check_list:
				do_not_check.append(m[1])

		for i in get_time_location:
			fake_bomb = i[4]
			station_name = i[2]
			timer_sql = "SELECT * FROM bombdettimer WHERE room = %s"
			c.execute(timer_sql, room)
			timer_list = list(c.fetchall())
			for j in timer_list:
				ttd = j[2]
			timer_10_sql = "SELECT * FROM `10secdrop` WHERE room = %s"
			c.execute(timer_10_sql, room)
			row_count = c.rowcount
			if row_count != 0:
				ttd = str(10)
				tensec_remove = "DELETE FROM `10secdrop` WHERE room = %s"
				c.execute(tensec_remove, room)
			if station_name in do_not_check and not fake_bomb:
				pass
			else:
				if not fake_bomb:
					do_not_check.append(station_name)
					ignore_add_sql = "INSERT INTO ignoreList (station, room) VALUES (%s, %s);"
					c.execute(ignore_add_sql, (station_name, room))
				query_update = "UPDATE bombsDeployed SET timeIncoming = %s WHERE id = %s ;"
				c.execute(query_update, (datetime.now() + timedelta(seconds=int(ttd)), i[0]))
				countdown(ttd, fake_bomb, i)
	do_not_check.clear()
	connection.close()


def countdown(ttd, fake=False, bomb=None):
	bmb_del = []
	player_locations = []
	connection = dataconnect()
	c = connection.cursor()
	time = int(ttd)
	while time > -1:

		if time == 0:
				if fake:
					# TODO, remove current bomb
					remove_sql = "DELETE FROM bombsDeployed WHERE id=%s;"
					c.execute(remove_sql, bomb[0])
					return
				bmb_det_sql = "SELECT * FROM bombDetect"
				c.execute(bmb_det_sql)
				bmb_det_list = list(c.fetchall())
				for i in bmb_det_list:
					bmb_del.append(i[1])
				player_locations_sql = "SELECT * FROM playerLocation WHERE EXISTS ( SELECT mac FROM TrackerNames)"
				c.execute(player_locations_sql)
				player_locations_list = list(c.fetchall())
				for j in player_locations_list:
					if j[1] in bmb_del:
						pass
					else:
						print("Player: " + j[1] + " Player Location: " + j[2])
						player_locations.append(j[2])
				bomb_location_sql = "SELECT * FROM bombsDeployed WHERE room = %s"
				c.execute(bomb_location_sql, room)
				bomb_location = list(c.fetchall())
				for k in bomb_location:
					do_release = "SELECT * FROM loosingTeam"
					c.execute(do_release)
					row_count = c.rowcount
					station_to_check = k[2]
					if row_count == 0:
						if station_to_check in player_locations:
							get_room_sql = "SELECT * FROM stationList WHERE name = %s"
							c.execute(get_room_sql, station_to_check)
							get_room_list = list(c.fetchall())
							for l in get_room_list:
								room_dead = l[2]
								kill_game = "INSERT INTO loosingTeam (team, station) VALUES (%s, %s);"
								c.execute(kill_game, (room_dead, station_to_check))
						else:
							play_add_sql = "INSERT INTO audiomanager (whattoplay, room) VALUES (%s, %s)"
							c.execute(play_add_sql, ("allclearstub", room))
					else:
						play_add_sql = "INSERT INTO audiomanager (whattoplay, room) VALUES (%s, %s)"
						c.execute(play_add_sql, ("allclearstub", room))

				time = time - 1
		else:
			if time == 5:
				play_add_sql = "INSERT INTO audiomanager (whattoplay, room) VALUES (%s, %s)"
				c.execute(play_add_sql, ("bombdroppingnew", room))
			print(time)
			time = time - 1
			sleep(1)

	connection.close()


while True:
	check_det()
