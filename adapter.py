# https://stackoverflow.com/a/61771563/13198229

# HTTP server will send the input string as it is to adapter
# adapter will once parse the string and then here onwards
# only json objects would be sent
# Request will have a priority instead of user (to handle C2C connections)
# to terminate a connection from HTTP server to adapter, send a string "terminate"
# to terminate a connection from adapter to pq, send a string "terminate"

from multiprocessing.connection import Listener, Client
import json
import time

time.sleep(4)

listener_port = 6000
# dictionary containing port numbers for different pq
port_numbers = {
    "instagram": 6001,
    "weather": 6002,
    "translate": 6003,
    "reverse": 6004,
    "C2C": 6005
}

# dictionary containing connections to priority queues
conn_a2pq = {}
for key, value in port_numbers.items():
    conn_a2pq[key] = Client(('localhost', value), authkey=b'secret password')

# accept a connection from HTTP server
listener = Listener(('localhost', listener_port), authkey=b'secret password')

running = True
while running:
    # data accepted from http server
    conn_s2a = listener.accept()
    print('connection accepted from', listener.last_accepted)
    msg = conn_s2a.recv()
    print(msg)
    if msg == "terminate":
        conn_s2a.close()
        running = False

        for conn in conn_a2pq.values():
            conn.send("terminate")
            print(f"terminate adapter {listener_port}")
            conn.close()  # close the subsequent connections to pqs

        break

        # data is a json object
    data = json.loads(msg)  # parse the string

    TypeofRequest = data["TypeofRequest"]  # redundent
    Receiver = data["Receiver"]
    # forward data to corresponding priority queue
    if TypeofRequest == "API":
        conn_a2pq[Receiver].send(data)
    else:
        conn_a2pq["C2C"].send(data)
    # conn_a2pq[Receiver].send(data)

# data received from HTTP server
# RequestID
# Username
# TypeofRequest - API for API call, C2C for Client to Client communication
# Receiver - API/Client to be contacted
# Payload - contains the payload / message // string object
# RequestPriority (user priority for API call and sum of clients' priority in case of C2C)