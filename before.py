from multiprocessing.connection import Client, Listener
import sys
from time import sleep
from random import randint


class bcolors:
    OK = '\033[92m'  #GREEN
    WARNING = '\033[93m'  #YELLOW
    FAIL = '\033[91m'  #RED
    RESET = '\033[0m'  #RESET COLOR


port_number = int(sys.argv[1])
sleep(4)

conn_before = Client(('localhost', port_number), authkey=b'secret password')
value = 0

while True:
    data = {
        "RequestID": value,
        "RequestPriority": randint(1, 5),
        "Content": value,
    }
    value += 1
    conn_before.send(data)
    reqid = data["RequestID"]
    reqpr = data["RequestPriority"]
    content = data["Content"]
    total_pr = 10 * reqpr - reqid
    print(bcolors.FAIL,
          f"sending | {reqid} | {reqpr} | {content} | {total_pr}",
          bcolors.RESET)
    sleep(1)
    if value == 10:
        conn_before.send("terminate")
        conn_before.close()
        break
