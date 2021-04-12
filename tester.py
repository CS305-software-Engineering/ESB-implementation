from multiprocessing.connection import Client
import time
import json

# Client 1
j = {"id": 81, "name": "sathwik"}
data = json.dumps(j)
conn = Client(('localhost', 6005), authkey=b'secret password')
conn.send(data)
time.sleep(1)

conn.send('terminate')
time.sleep(1)

conn.close()