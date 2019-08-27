#!/usr/bin/python
import signal
import SocketServer
from time import time, sleep
import os
import subprocess


subprocess.Popen("sudo python rebootready.py", shell=True)
sleep(1)
subprocess.Popen("sudo python radio.py", shell=True)
sleep(1)


