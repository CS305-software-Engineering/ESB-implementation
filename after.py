from multiprocessing.connection import Client, Listener
import sys
from time import sleep


class bcolors:
    OK = '\033[92m'  #GREEN
    WARNING = '\033[93m'  #YELLOW
    FAIL = '\033[91m'  #RED
    RESET = '\033[0m'  #RESET COLOR


port_number = int(sys.argv[1])
sleep(2)

listener = Listener(('localhost', port_number), authkey=b'secret password')
conn_after = listener.accept()
print(bcolors.OK, "connection accepted in after.py", bcolors.RESET)

while True:
    data = conn_after.recv()
    if data == "terminate":
        print(bcolors.OK, "Terminated", bcolors.RESET)
        break
    reqid = data["RequestID"]
    reqpr = data["RequestPriority"]
    content = data["Content"]
    total_pr = 10 * reqpr - reqid
    print(bcolors.OK, f"received | {reqid} | {reqpr} | {content} | {total_pr}",
          bcolors.RESET)  # green print
    sleep(3)
    conn_after.send("free")