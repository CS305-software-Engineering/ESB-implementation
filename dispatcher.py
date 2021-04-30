from multiprocessing.connection import Listener, Client
import time
import sys

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')


def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database=str(MYSQL_DB),
                                       user='root',
                                       password=str(MYSQL_PASSWORD))
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


connect()

time.sleep(2)
# port on which processing module is sending data
listener_port = int(sys.argv[1])
# port on which HTTP server is listening
http_port = int(sys.argv[2])

listener = Listener(('0.0.0.0', listener_port), authkey=b'secret password')
# sender = Client(('0.0.0.0', http_port), authkey=b'secret password')
running = True
con = listener.accept()
while running:
    msg = con.recv()
    if msg == 'terminate':
        con.close()
        print(f"terminate dispatcher {listener_port}")
        # sender.send(msg)
        # sender.close()
        running = False
        break
    # sender.send(msg)
    print('write msg to database if msg is not terminate')
