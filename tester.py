from multiprocessing.connection import Client
import time
import json
from curr_time import get_curr_time

time.sleep(10)
# Client 1
j = {
    "RequestID": 81,
    "Username": "SathwikB",
    "TypeofRequest": "API",
    "Receiver": "weather",
    "Payload": "Mumbai",
    "RequestPriority": 100,
    "InitialTimestamp": get_curr_time()
}
j1 = {
    "RequestID": 1,
    "Username": "SathwikB",
    "TypeofRequest": "API",
    "Receiver": "translate",
    "Payload": "Kaise ho",
    "RequestPriority": 10000,
    "InitialTimestamp": get_curr_time()
}

data = json.dumps(j)
data2 = json.dumps(j1)
conn = Client(('localhost', 6000), authkey=b'secret password')
conn.send(data)

# print("sending", data)
time.sleep(5)
conn.send(data2)
# print("sending", data2)
data = 'terminate'
time.sleep(20)
conn.send(data)
# print("sending", data)
conn.close()
while True:
    print("looping")
    time.sleep(3)