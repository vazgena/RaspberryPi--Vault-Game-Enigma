#!/usr/bin/python
import RPi.GPIO as GPIO

import os
import SocketServer

from time import sleep

import subprocess
subprocess.Popen("python sendstatus.py radio alive 9995", shell=True)

def start():
    subprocess.Popen("python static.py", shell=True)
    sleep(.1)
    subprocess.Popen("python station1.py", shell=True)
    sleep(.1)
    subprocess.Popen("python station2.py", shell=True)
    sleep(.1)
    subprocess.Popen("python station3.py", shell=True)
    sleep(.1)
    sleep(3600)
    complete()

def complete():
    subprocess.Popen("reboot", shell=True)


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
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

        if self.data == "radio activate":
            subprocess.Popen("python sendstatus.py radio active 9995", shell=True)
            start()
        if self.data =="radio reboot":
            subprocess.Popen("python sendstatus.py radio dead 9995", shell=True)
            subprocess.Popen("reboot", shell=True)


if __name__ == "__main__":
    try:
        HOST, PORT = '', 9995
        # instantiate the server, and bind to localhost on port 9999
        server = SocketServer.TCPServer((HOST, PORT), MyTCPSocketHandler)
        # activate the server
        # this will keep running until Ctrl-C
        server.serve_forever()
    except SystemExit:
        GPIO.cleanup()
        raise