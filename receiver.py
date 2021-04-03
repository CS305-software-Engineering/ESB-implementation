# # https://stackoverflow.com/a/61771563/13198229

# from multiprocessing.connection import Listener
# import json

# listener = Listener(('localhost', 6969), authkey=b'secret password')
# running = True
# while running:
#     conn = listener.accept()
#     print(type(conn))
#     print('connection accepted from', listener.last_accepted)
#     while True:
#         msg = conn.recv()

#         print(msg)
#         if msg['terminate'] == False:
#             conn.close()
#             break
#         if msg['terminate'] == True:
#             conn.close()
#             running = False
#             break
# listener.close()

from multiprocessing.connection import Listener
from time import sleep

listener = Listener(('localhost', 6000), authkey=b'secret password')
running = True
while running:
    conn = listener.accept()
    print("accepted")
    print('connection accepted from', listener.last_accepted)
    sleep(2)
    while True:
        # sleep(3)
        # print("waking up")
        msg = conn.recv()
        # print("received")
        print(msg)
        if msg == 'close connection':
            conn.close()
            break
        if msg == 'close server':
            conn.close()
            running = False
            break
listener.close()
