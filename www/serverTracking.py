from time import sleep
import numpy as np
import scipy.signal
from scipy.spatial.distance import cdist
from scipy.optimize import minimize
from pymysql import InternalError, connect
from datetime import datetime


dbuser = 'game'
dbpass = 'h95d3T7SXFta'

# smoothing window size
n = 3
# target value, counting from the end. affects lag, -2 recommended
n_2 = -2  # int(np.floor(n/2)) #


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
		# TODO: hotfix for BMB1, BMB2
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


def new_loop():
	connection = dataconnect()
	c = connection.cursor()
	get_locations = "SELECT mac, station FROM trackers;"
	c.execute(get_locations)
	listed_trackers = list(c.fetchall())

	mac_map = {}

	for k in listed_trackers:
		mac = k[0]
		station = k[1]
		if mac not in mac_map:
			mac_map[mac] = []
		mac_map[mac].append(station)

	sql_query = "SELECT value FROM trackers_value WHERE mac=%s AND station=%s ORDER BY timestamp DESC LIMIT %s;"

	for mac in mac_map:
		value_array = np.zeros((len(mac_map[mac]), n))
		for i, station in enumerate(mac_map[mac]):
			if station in ['BMB1', 'BMB2']:
				continue
			c.execute(sql_query, (mac, station, n))
			listed_value = list(c.fetchall())
			values = [value[0] for value in listed_value]
			if len(values) < n:
				continue
			value_array[i, :] = values

		# mean_values_old = np.mean(value_array, axis=1)
		# j_old = np.argmax(mean_values_old)
		mean_values = scipy.signal.medfilt(value_array, kernel_size=(1, n))
		# j = np.argmax(mean_values[:, n_2])
		j = np.argmin(mean_values[:, n_2])

		# mean_value = "{:.2f}".format(mean_values[j])
		mean_value = "{:.2f}".format(mean_values[j, n_2])
		location = mac_map[mac][j]

		bmb_check = "SELECT * FROM ignorePlayerList WHERE mac = %s;"
		# TODO: check location/mac
		# c.execute(bmb_check, mac)
		c.execute(bmb_check, location)
		row_count = c.rowcount
		if row_count == 0:
			insert_location_sql = "INSERT INTO playerLocation (mac, location, bleSignal) " \
								  "VALUES (%s,%s,%s) ON DUPLICATE KEY " \
								  "UPDATE mac = %s, location = %s, bleSignal = %s";
			c.execute(insert_location_sql, (mac, location, mean_value,
											mac, location, mean_value))

	sql_request_remove = "DELETE FROM trackers_value WHERE timestamp < DATE_SUB(NOW(), INTERVAL 1 MINUTE);"
	c.execute(sql_request_remove)
	connection.close()


def mse(x, distances, locations):
	c_dist = cdist(x.reshape((1, 2)), locations)
	error_dist = distances - c_dist
	error_dist *= distances
	error_dist[error_dist > 0] = error_dist[error_dist > 0]/2
	mse = np.square(error_dist).mean()
	return mse


def optimization(initial_location, locations, distances):
	result = minimize(
		mse,  # The error function
		initial_location,  # The initial guess
		args=(locations, distances),  # Additional parameters for mse
		method='L-BFGS-B',  # The optimisation algorithm
		options={
			'ftol': 1e-5,  # Tolerance
			'maxiter': 1e+7  # Maximum iterations
		})
	location = result.x
	return location



while True:
	# loop()
	new_loop()