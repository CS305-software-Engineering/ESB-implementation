from multiprocessing.connection import Listener, Client
import json
from rapidapi import str_rev_api, translate_api, weather_api, insta_api
listener = Listener(('locahost', 6001), authkey=b'secret password')
running = True
while running:
    conn_2ia = listener.accept()
    print('connection accepted from', listener.last_accepted)
    msg = conn_2ia.recv()
    if msg == 'terminate':
        conn_2ia.close()
        running = False
    else:
        # process api
        # create client to seng to dispacter
        # close the client connection
        # close this connection
        d = json.loads(msg)
        username = d['Payload']
        Api_response = insta_api(username)
        d['Api_response'] = Api_response
        msg = json.dumps(d)
        conn_2dp = Client(('localhost', 6501), authkey=b'secret password')
        conn_2dp.send(msg)  # is api_reponse a json object
        conn_2dp.close()
listener.close()
