from multiprocessing.connection import Listener
import json
from socket import *

sock = socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
listener = Listener(('localhost', 8600), authkey=b'secret password')
running = True
while running:
    conn = listener.accept()
    print('connection accepted from', listener.last_accepted)
    while True:
        msg = conn.recv()
        #msg=msg.decode("utf-8")
        print("all clear",msg)
        try:
            d = json.loads(msg)
            print(d["id"])
        except:
            if msg == 'terminate':
                conn.close()
                running = False
                break
