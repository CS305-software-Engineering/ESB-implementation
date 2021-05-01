from multiprocessing.connection import Listener, Client
import json
from utils import find_priority_of_request


def start_adapter_connection():
    global conn_s2a
    conn_s2a = Client(('localhost', 6000), authkey=b'secret password')
    print("connection to adapter established")


def RequestSender(username, receiver, message, initial_timestamp, reqID):
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
    conn_s2a.send(data)