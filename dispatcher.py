from multiprocessing.connection import Listener, Client
import time
import sys
import json
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
            return conn

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


conn = connect()

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
    data = json.loads(msg)
    reqID = data["RequestID"]
    username = data["Username"]
    receiver = data["Receiver"]
    initial_timestamp = data["InitialTimestamp"]
    final_timestamp = time.time()
    message = data["Payload"]
    response = data["Api_response"]
    typeofreq = data["TypeofRequest"]
    
    cur = conn.cursor()
    cur.execute('INSERT into Pending(RequestID,Username,Receiver,RequestPayload,InitialTimestamp) values(%s,%s,%s,%s,%s)',(str(reqID),str(username),str(receiver),str(message),initial_timestamp))
    
    cur.execute('INSERT into AckLogs(RequestID,Username,TypeofRequest,Receiver,RequestPayload,InitialTimestamp,FinalTimestamp,ServiceResponseStatus,ReturnResponseStatus) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(str(reqID),str(username),str(typeofreq),str(receiver),str(message),initial_timestamp,final_timestamp,200,200))