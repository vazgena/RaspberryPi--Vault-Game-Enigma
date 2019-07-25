from time import sleep
from pymysql import InternalError, connect


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


def run_once():
	connection = dataconnect()
	c = connection.cursor()
	try:
		track_trunk = "TRUNCATE TABLE trackers"
		c.execute(track_trunk)
		track_trunk = "TRUNCATE TABLE playerLocation"
		c.execute(track_trunk)
	except InternalError:
		pass
	connection.close()


run_once()


def loop():
	avg = ""
	saved = []
	connection = dataconnect()
	c = connection.cursor()
	get_locations = "SELECT mac FROM trackers"
	c.execute(get_locations)
	listed_trackers = list(c.fetchall())
	trackers_set = set(listed_trackers)
	listed_unique_trackers = list(trackers_set)

	for k in listed_unique_trackers:
		player_trackers = "SELECT * FROM trackers WHERE mac = %s AND station != 'BMB1' AND station != 'BMB2';"
		c.execute(player_trackers, k)
		compareable_list = list(c.fetchall())
		for l in compareable_list:
			try:
				if l[3] == "BMB1":
					avg = float(l[4])
					avg = avg + 2
				else:
					avg = float(l[4])
				if float(avg) >= float(saved[3]):
					saved = (l[1], l[2], l[3], avg, l[5])
				else:
					pass
			except:
				saved = (l[1], l[2], l[3], avg, l[5])
				pass

		try:
			if float(saved[3]) > 60:
				bmb_check = "SELECT * FROM ignorePlayerList WHERE mac = %s"
				c.execute(bmb_check, saved[2])
				row_count = c.rowcount
				if row_count == 0:
					insert_location_sql = "INSERT INTO playerLocation (mac, location, bleSignal) " \
										  "VALUES (%s,%s,%s) ON DUPLICATE KEY " \
										  "UPDATE mac = %s, location = %s, bleSignal = %s"
					c.execute(insert_location_sql, (saved[1], saved[2], saved[3],
													saved[1], saved[2], saved[3]))
		except:
			print(saved)
			pass
		saved = []

	connection.close()


while True:
	loop()
