from multiprocessing.connection import Listener, Client
import time
import sys

time.sleep(2)
# port on which processing module is sending data
listener_port = int(sys.argv[1])
# port on which HTTP server is listening
http_port = int(sys.argv[2])

listener = Listener(('0.0.0.0', listener_port), authkey=b'secret password')
# sender = Client(('0.0.0.0', http_port), authkey=b'secret password')
running = True
con = listener.accept()
while running:
    msg = con.recv()
    if msg == 'terminate':
        con.close()
        print(f"terminate dispatcher {listener_port}")
        # sender.send(msg)
        # sender.close()
        running = False
        break
    # sender.send(msg)
    print("to be put into db for communication")
