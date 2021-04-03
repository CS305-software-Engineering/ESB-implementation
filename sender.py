# https://stackoverflow.com/a/61771563/13198229

# from multiprocessing.connection import Client
# import time
# import json

# data_set = {"key1": [1, 2, 3], "key2": [4, 5, 6], "terminate": False}

# # Client 1
# conn = Client(('localhost', 6969), authkey=b'secret password')
# conn.send(data_set)
# time.sleep(1)
# conn.send('close connection')
# conn.close()

# time.sleep(1)
# data_set = {"key1": [1, 2, 3], "key2": [4, 5, 6], "terminate": True}

# # Client 2
# conn = Client(('localhost', 6969), authkey=b'secret password')
# conn.send(data_set)
# conn.send('close server')
# conn.close()

from multiprocessing.connection import Client
import time

# Client 1
conn = Client(('localhost', 6000), authkey=b'secret password')
conn.send('===========first message===========')
conn.send('===========second message===========')
conn.send('===========third message===========')
# time.sleep(5)
conn.send('===========fourth message===========')
conn.send('===========fifth message===========')

for _ in range(100000):
    conn.send(str(_) + " " + str(_) + " " + str(_) + " " + str(_))

conn.send('close connection')
conn.close()
time.sleep(1)

# # Client 2
# conn = Client(('localhost', 6000), authkey=b'secret password')
# conn.send('bar')
# conn.send('close server')
# conn.close()