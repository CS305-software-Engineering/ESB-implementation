# one adaptor parses the information and forwards to necessary priority_queues
# this particular program will have 5 instances

from multiprocessing.connection import Client, Listener
import json
import sys

# // TODO => DONE take command line args to decide the port number of listener
# this is for one of the 5 branches in the flow
# TODO decide the port numbers
# listener_port = 6000
# # dictionary containing port numbers for different processing modules
# port_numbers = {
#     "instagram": 6001,
#     "weather": 6002,
#     "translate": 6003,
#     "C2C": 6004
# }
listener_port = int(sys.argv[1])
processor_port = int(sys.argv[2])

listener_a2pq = Listener(('localhost', listener_port),
                         authkey=b'secret password')
print('connection accepted from', listener_a2pq.last_accepted)

# accept connection from adapter
conn_a2pq = listener_a2pq.accept()
# make connection to processing module (maybe not needed)
conn_pq2p = Client(('localhost', processor_port), authkey=b'secret password')

# listener_p2pq = Listener(('localhost', processor_port),
#                          authkey=b'secret password')

# for checking if the processor is busy or not this is needed
# maybe not
# conn_p2pq = listener_p2pq.accept()
processor_busy = False
# If not this then try to use shared memory to modify this processor_busy variable

# TODO maintain a priority queue on RequestPriority and RequestID
# TODO maintain a map from RequestID to Json DATA

RequestID_to_json_data = {}

running = True
while running:
    # precent hanging in this location
    # https://stackoverflow.com/a/20290016/13198229
    # if works then no need for shared memory and mutex
    msg = conn_a2pq.recv()
    if msg == "terminate":
        pass  # TODO

    data = msg  # this is a json object

    # insert into map
    # insert into priority_queue
    # if queue.size then pass the data to processing module if processing module is not busy

    # start mutex
    if not processor_busy:
        # send data to processing module
        # TODO
        # conn_pq2p.send(RequestID_to_json_data[from the top of PQ])
        processor_busy = True  # after sending data, processor will be busy
    # mutex close

# priority_queue will keep on receiving requests from adapter.py
# but will send data to processor only if it is free to do so

# since it is a client server relation
# hence feedbacks can be used from processing module
# to check whether it is available to process next query
# if yes then send next query