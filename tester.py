from multiprocessing.connection import Client
import time
import json
from socket import *

sock = socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# Client 1
j = {
    "RequestID": 81,
    "Username": "SathwikB",
    "TypeofRequest": "API",
    "Receiver": "instagram",
    "Payload": "nagasrikarkanniganti",
    "RequestPriority": 100
}
j1 = {
    "RequestID": 1,
    "Username": "SathwikB",
    "TypeofRequest": "API",
    "Receiver": "instagram",
    "Payload": "abhayypatil",
    "RequestPriority": 10000
}

data = json.dumps(j)
data2=json.dumps(j)
conn = Client(('localhost', 6000), authkey=b'secret password')
conn.send(data)
print("sending", data)
conn.send(data2)
print("sending", data2)
data = 'terminate'

conn.send(data)
print("sending", data)

conn.close()