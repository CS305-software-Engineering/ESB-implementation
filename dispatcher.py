from multiprocessing.connection import Listener,Client
import json
import time
from socket import *
import sys

sock=socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# for instagram api
listener_port = int(sys.argv[1])  #port on which processing module is sending data
http_port = int(sys.argv[2])      #port on which HTTP server is listening

listener = Listener(('localhost', listener_port), authkey=b'secret password')
sender = Client(('localhost', http_port), authkey=b'secret password')
running=True
while running:
    con=listener.accept()
    msg=con.recv()
    print(msg)
    if msg=="terminate":
        con.close()
        sender.send(msg)
        sender.close()
        running=False
        break
    sender.send(msg)
