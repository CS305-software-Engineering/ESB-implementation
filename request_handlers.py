from multiprocessing.connection import Listener, Client
import json
from utils import find_priority_of_request

# def connect_http_to_adapter():
#     conn_s2a = Client(('localhost', 6000), authkey=b'secret password')
#     print("connection from http server to adapter established")
#     return conn_s2a


def Terminator():
    conn_s2a = Client(('localhost', 6000), authkey=b'secret password')
    conn_s2a.send("terminate")


def RequestSender(username, receiver, message, initial_timestamp, reqID):
    conn_s2a = Client(('localhost', 6000), authkey=b'secret password')
    print("connection from http server to adapter established")
    data = {}
    if receiver in ['reverse', 'instagram', 'translate', 'weather']:
        data["TypeofRequest"] = "API"
    else:
        data["TypeofRequest"] = "C2C"
    data["Receiver"] = receiver
    data["Username"] = username
    data["Payload"] = message
    data["InitialTimestamp"] = initial_timestamp
    data["RequestID"] = reqID
    data["RequestPriority"] = find_priority_of_request(reqID, username)
    conn_s2a.send(json.dumps(data))
    conn_s2a.send("terminate")