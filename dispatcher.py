from multiprocessing.connection import Listener, Client
import time
import sys
import json
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from curr_time import get_curr_time

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

    # finally:
    #     if conn is not None and conn.is_connected():
    #         conn.close()


conn = connect()

time.sleep(2)

# port on which processing module is sending data
listener_port = int(sys.argv[1])
# port on which HTTP server is listening
http_port = int(sys.argv[2])  #! deprecated

listener = Listener(('localhost', listener_port), authkey=b'secret password')
# sender = Client(('localhost', http_port), authkey=b'secret password')

print('in dispathcer connection accepted from', listener.last_accepted,
      http_port)
running = True
con = listener.accept()
while running:
    msg = con.recv()
    if msg == 'terminate':
        con.close()
        conn.close()
        print(f"terminate dispatcher {listener_port}")
        # sender.send(msg)
        # sender.close()
        running = False
        break

    data = json.loads(msg)
    reqID = data["RequestID"]
    typeofreq = data["TypeofRequest"]
    username = data["Username"]
    receiver = data["Receiver"]
    initial_timestamp = data["InitialTimestamp"]
    final_timestamp = get_curr_time()
    message = data["Payload"]
    response2 = data["Api_response"]
    response1 = json.loads(response2)
    response = {}
    
    if receiver == "instagram":
        if "status" in response1 and response1["status"] == "fail":
            response = json.dumps({"status":"fail"})
        else:
            bio = response1["biography"]
            followers = response1["edge_followed_by"]["count"]
            following = response1["edge_follow"]["count"]
            response = json.dumps({"biography":bio,"followers":followers,"following":following})
        
    elif receiver == "translate":
        lang_code = response1["data"]["detections"][0][0]["language"]
        confidence = response1["data"]["detections"][0][0]["confidence"]
        f = open('static/languages_codes.json')
        data = json.load(f)
        lang_name=""
        for i in data["code2lang"]:
            if (i["alpha2"] == lang_code):
                lang_name = i["English"]
                break
        response = json.dumps({"language":lang_name,"confidence":confidence})
        print(response)
        
    elif receiver == "weather":
        if (response2[0] == 't'):
            str_out = response2[4:]
            json_dict = json.loads(str_out)
            out = []
            out.append(json_dict["weather"][0]["main"])
            out.append(json_dict["weather"][0]["description"])
            out.append(json_dict["main"]["temp"])
            out.append(json_dict["main"]["feels_like"])
            out.append(json_dict["main"]["temp_min"])
            out.append(json_dict["main"]["temp_max"])
            out.append(json_dict["main"]["pressure"])
            out.append(json_dict["main"]["humidity"])
            response = json.dumps({"main":out[0],"desc":out[1],"temp":out[2],"feels":out[3],"temp_min":out[4],"temp_max":out[5],"pressure":out[6],"humidity":out[7]})  
        else:
            response = json.dumps({"message":"OOPS! City not found"})
            
    else:
        response = response2

    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT into Pending(RequestID,Username,Receiver,RequestPayload,InitialTimestamp,Response) values(%s,%s,%s,%s,%s,%s)',
            (str(reqID), str(username), str(receiver), str(message),
             initial_timestamp, str(response)))
        conn.commit()
        print("wrote to Pending")

        cur.execute(
            'INSERT into AckLogs(RequestID,Username,TypeofRequest,Receiver,RequestPayload,Response,InitialTimestamp,FinalTimestamp,ServiceResponseStatus,ReturnResponseStatus) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (str(reqID), str(username), str(typeofreq), str(receiver),
             str(message), str(response), initial_timestamp, final_timestamp,
             200, 200))
        conn.commit()
        print("wrote to AckLogs")
        cur.close()
    except Exception as exp:
        print("unable to write to db")
        print(exp)
