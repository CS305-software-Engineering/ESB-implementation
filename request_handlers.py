from multiprocessing.connection import Listener, Client
import json
from utils import find_priority_of_request

conn_s2a = Client(('localhost', 6000), authkey=b'secret password')
    
def RequestSender(username,receiver,message,initial_timestamp,reqID):
    data = {}
    if receiver in ['reverse','instagram','translate','weather']:
        data["TypeofRequest"] = "C2A"
    else:
        data["TypeofRequest"] = "C2C"
    data["Receiver"] = receiver
    data["Username"] = username
    data["Payload"] = message
    data["InitialTimestamp"] = initial_timestamp
    data["RequestID"] = reqID
    data["RequestPriority"] = find_priority_of_request(reqID,username)
    conn_s2a.send(data)