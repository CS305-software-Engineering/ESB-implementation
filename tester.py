from multiprocessing.connection import Client
import time
import json
from socket import *
time.sleep(10)
sock = socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# Client 1
j = {
    "RequestID": 81,
    "Username": "SathwikB",
    "TypeofRequest": "API",
    "Receiver": "weather",
    "Payload": "Mumbai",
    "RequestPriority": 100
}
j1 = {
    "RequestID": 1,
    "Username": "SathwikB",
    "TypeofRequest": "API",
    "Receiver": "weather",
    "Payload": "Hyderabad",
    "RequestPriority": 10000
}

data = json.dumps(j)
data2=json.dumps(j1)
conn = Client(('localhost', 6000), authkey=b'secret password')
conn.send(data)

print("sending", data)
time.sleep(5)
conn.send(data2)
print("sending", data2)
data = 'terminate'
time.sleep(25)
conn.send(data)
print("sending", data)
conn.close()