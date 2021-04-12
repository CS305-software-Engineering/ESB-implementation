from multiprocessing.connection import Client
import time
import json
from socket import *

sock = socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# Client 1
j = {"id": 81, "Payload": "warangal"}
data = json.dumps(j)
conn = Client(('localhost', 8002), authkey=b'secret password')
print("sending", data)
conn.send(data)

data = 'terminate'
print("sending",data)
conn.send(data)


conn.close()