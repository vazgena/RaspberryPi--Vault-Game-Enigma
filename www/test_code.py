import os
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from pymysql import InternalError, connect
from random import choice


# Variables
app = Flask(__name__)
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


def test_timer():
    atkroom = '2'
    itemID = '8'
    query = "INSERT INTO marketOwned (itemID, text, numberOwned, team) VALUES (%s, %s, %s, %s);"
    connection = data_connect()
    c = connection.cursor()
    c.execute(query, (itemID, "", "1", atkroom))
    connection.close()

if __name__ == "__main__":
    test_timer()
