import signal
import SocketServer
import os
import sys
import subprocess
from time import sleep 

class MyTCPSocketHandler(SocketServer.BaseRequestHandler):
	"""
	The RequestHandler class for our server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""

	def handle(self):
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		datasent = self.data.split(" ")
		# just send back the same data, but upper-cased
		self.request.sendall(self.data.upper())

		if datasent[0] =="reboot":
			process = subprocess.Popen("python sendstatus.py dead", shell=True)
			process.wait()
			subprocess.Popen("reboot", shell=True)
		if datasent[0] =="restart":
			commandsend1 = "sudo pkill -1 -f station1.py -e"
			commandsend2 = "sudo pkill -1 -f station2.py -e"
			commandsend3 = "sudo pkill -1 -f station3.py -e"
			commandsend4 = "sudo pkill -1 -f static.py -e"
			commandsend5 = "sudo pkill -1 -f radio.py -e"
			os.system(commandsend1)
			os.system(commandsend2)
			os.system(commandsend3)
			os.system(commandsend4)
			os.system(commandsend5)
			subprocess.Popen("python sendstatus.py radio dead 9999", shell=True)
			sleep(.3)
			subprocess.Popen("sudo python radio.py", shell=True)
		if datasent[0] =="crash":
			commandsend1 = "sudo pkill -1 -f station1.py -e"
			commandsend2 = "sudo pkill -1 -f station2.py -e"
			commandsend3 = "sudo pkill -1 -f station3.py -e"
			commandsend4 = "sudo pkill -1 -f static.py -e"
			commandsend5 = "sudo pkill -1 -f radio.py -e"
			os.system(commandsend1)
			os.system(commandsend2)
			os.system(commandsend3)
			os.system(commandsend4)
			os.system(commandsend5)
			subprocess.Popen("python sendstatus.py radio dead 9999", shell=True)

if __name__ == "__main__":
	HOST, PORT = '', 999
	# instantiate the server, and bind to localhost on port 999
	server = SocketServer.TCPServer((HOST, PORT), MyTCPSocketHandler)
	# activate the server
	# this will keep running until Ctrl-C
	server.serve_forever()
	firstload()
