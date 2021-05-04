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
        conn = mysql.connector.connect(host='us-cdbr-east-03.cleardb.com',
                                       database=str(MYSQL_DB),
                                       user='b98a15b202597c',
                                       password=str(MYSQL_PASSWORD))
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn

    except Error as e:
        print(e)

    # finally:
    #     if conn is not None and conn.is_connected():
    #         conn.close()


time.sleep(1)

# port on which processing module is sending data
listener_port = int(sys.argv[1])
# port on which HTTP server is listening
http_port = int(sys.argv[2])  # ! deprecated

listener = Listener(('localhost', listener_port), authkey=b'secret password')
# sender = Client(('localhost', http_port), authkey=b'secret password')

print('in dispatcher connection accepted from', listener.last_accepted,
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
    # print("in dispatcher", type(response2))
    # print("in dispatcher", response2[5:-1])
    # response1 = json.loads(response2[5:-1])
    # response = {}
    service_resp = 200
    if receiver == "instagram":
        response1 = json.loads(response2)
        response = {}
        if "status" in response1 and response1["status"] == "fail":
            response = json.dumps({"status": "fail"})
            service_resp = 404
        elif "message" in response1:
            response = json.dumps({"status": "unauthorized"})
            service_resp = 401
        else:
            bio = response1["biography"]
            followers = response1["edge_followed_by"]["count"]
            following = response1["edge_follow"]["count"]
            response = json.dumps({
                "biography": bio,
                "followers": followers,
                "following": following
            })

    elif receiver == "translate":
        response1 = json.loads(response2)
        response = {}
        if "message" in response1:
            response = json.dumps({"status": "unauthorized"})
            service_resp = 401
        else:
            lang_code = response1["data"]["detections"][0][0]["language"]
            confidence = response1["data"]["detections"][0][0]["confidence"]
            f = open('static/languages_codes.json')
            data = json.load(f)
            lang_name = ""
            for i in data["code2lang"]:
                if (i["alpha2"] == lang_code):
                    lang_name = i["English"]
                    break
            response = json.dumps({
                "language": lang_name,
                "confidence": confidence
            })

    elif receiver == "weather":
        response = {}
        if (response2[0] == 't'):
            str_out = response2[5:-1]
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
            response = json.dumps({
                "main": out[0],
                "desc": out[1],
                "temp": out[2],
                "feels": out[3],
                "temp_min": out[4],
                "temp_max": out[5],
                "pressure": out[6],
                "humidity": out[7]
            })
        else:
            response1 = json.loads(response2)
            if "message" in response1:
                response = json.dumps({"message": "unauthorized"})
                service_resp = 401
            else:
                response = json.dumps({"message": "OOPS! City not found"})
                service_resp = 404

    elif receiver == "reverse":
        response = response2

    else:  # for c2c
        response = response2

    try:
        conn = connect()

        # time.sleep(5) # to demonstrate the usage of fetching resulst in API calling
        cur = conn.cursor()
        cur.execute(
            'INSERT into Pending(RequestID,Username,Receiver,RequestPayload,InitialTimestamp,Response) values(%s,%s,%s,%s,%s,%s)',
            (str(reqID), str(username), str(receiver), str(message),
             initial_timestamp, str(response)))
        conn.commit()
        print("in dispatcher wrote to Pending")

        cur.execute(
            'INSERT into AckLogs(RequestID,Username,TypeofRequest,Receiver,RequestPayload,Response,InitialTimestamp,FinalTimestamp,ServiceResponseStatus,ReturnResponseStatus) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (str(reqID), str(username), str(typeofreq), str(receiver),
             str(message), str(response), initial_timestamp, final_timestamp,
             service_resp, 0))
        conn.commit()

        cur.execute(
            "DELETE FROM Pending WHERE InitialTimestamp < (NOW() - 600);")
        # this is for 60 * 10 that is 10 minutes
        conn.commit()
        print("in dispatcher wrote to AckLogs")
        cur.close()
    except Exception as exp:
        print("in dispatcher unable to write to db")
        print(exp)
