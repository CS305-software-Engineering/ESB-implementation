from multiprocessing.connection import Listener, Client
import json
listener = Listener(('locahost', 6005), authkey=b'secret password')
running = True
while running:
    conn_c2c = listener.accept()
    print('connection accepted from', listener.last_accepted)
    msg = conn_c2c.recv()
    if msg == 'terminate':
        conn_c2c.close()
        running = False
    else:
        # process api
        # create client to seng to dispacter
        # close the client connection
        # close this connection
        d = json.loads(msg)
        # need to check if client is active of not
        client_message = d['Payload']
        d['Api_response'] = client_message
        msg = json.dumps(d)
        conn_2dp = Client(('localhost', 6505), authkey=b'secret password')
        conn_2dp.send(msg)  # is api_reponse a json object
        conn_2dp.close()
listener.close()
