# one adapter parses the information and forwards to necessary priority_queues
# this particular program will have 5 instances

from multiprocessing.connection import Client, Listener
import sys
from max_heap import *
import time

time.sleep(3)
listener_port = int(sys.argv[1])
processor_port = int(sys.argv[2])

listener_a2pq = Listener(('localhost', listener_port),
                         authkey=b'secret password')

# make connection to processing module (maybe not needed)
conn_pq2p = Client(('localhost', processor_port), authkey=b'secret password')

# accept connection from adapter
conn_a2pq = listener_a2pq.accept()
print('priority_queue connection accepted from', listener_a2pq.last_accepted,
      listener_port)
conn_a2pq_active = True

processor_busy = False

RequestID_to_json_data = {}  # map

# top => max(10 * request_priority - requestID, -RequestID)
# since requestIDs are generated serially, hence this will prevent starvation
priority_queue = max_heap()

running = True
while running:
    # for active adapter connection, keep receiving data
    if conn_a2pq_active:
        # only do if something is present to receive
        if conn_a2pq.poll():  # to make it unblockale
            msg = conn_a2pq.recv()
            if msg == "terminate":  # continue while the pq is not empty
                print(f"terminate priority queue {listener_port}")
                conn_a2pq_active = False
                conn_a2pq.close()
                continue

            data = msg  # this is a json object

            # insert into map
            RequestID_to_json_data[data["RequestID"]] = data
            # insert into priority_queue
            RequestPriority = data["RequestPriority"]
            RequestID = data["RequestID"]

            # to prevent starvation use RequestID also
            priority_queue.push([10 * RequestPriority - RequestID, -RequestID])

    # if queue.size then pass the data to processing module if processing module is not busy
    if not processor_busy:
        if not priority_queue.empty():
            # take the highest priority process
            QueueTop = priority_queue.pop()
            TopRequestID = -QueueTop[1]
            # send data to processing module
            conn_pq2p.send(RequestID_to_json_data[TopRequestID])
            # remove top request from map
            RequestID_to_json_data.pop(TopRequestID)
            # after sending data, processor will be busy
            processor_busy = True

        # if priority_queue is empty and processor no busy and connection from adapter has already been terminated
        # then close the communication to processing module
        elif not conn_a2pq_active:
            conn_pq2p.send("terminate")
            conn_pq2p.close()
            running = False
            break

    if conn_pq2p.poll():
        msg = conn_pq2p.recv()
        # make it non blocking
        if (msg == "free"):
            processor_busy = False

# priority_queue will keep on receiving requests from adapter.py
# but will send data to processor only if it is free to do so

# since it is a client server relation
# hence feedbacks can be used from processing module
# to check whether it is available to process next query
# if yes then send next query