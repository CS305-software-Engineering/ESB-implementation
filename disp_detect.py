from multiprocessing.connection import Listener,Client
import json
import time
from socket import *

sock=socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# for instagram api
listen_port=8052
send_port=4002 #HTTP server

listener = Listener(('localhost', listen_port), authkey=b'secret password')
sender = Client(('localhost', send_port), authkey=b'secret password')
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
