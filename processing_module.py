from multiprocessing.connection import Listener, Client
from socket import *
import json
import sys
from rapidapi import str_rev_api, translate_api, weather_api, insta_api
input_ports = {
    "instagram": 8001,
    "weather": 8002,
    "translate": 8003,
    "reverse": 8004,
    "c2c": 8005
}

processor_port = int(sys.argv[1])
dispatcher_port = int(sys.argv[2])
listener = Listener(('0.0.0.0', processor_port), authkey=b'secret password')
conn_2dp = Client(('0.0.0.0', dispatcher_port), authkey=b'secret password')
running = True
conn_2ia = listener.accept()
while running:
    print('connection accepted from', listener.last_accepted)
    msg = conn_2ia.recv()
    print(msg)
    if msg == 'terminate':
        conn_2dp.send('terminate')
        conn_2ia.close()
        running = False
    else:
        # process api
        # create client to seng to dispacter
        # close the client connection
        # close this connection
        #message = json.loads(msg)
        message=msg
        if processor_port == input_ports["instagram"]:  # call instagram api
            username = message['Payload']
            Api_response = insta_api(username)
            message['Api_response'] = Api_response

        elif processor_port == input_ports["weather"]:  # call weather api
            location = message['Payload']
            Api_response = weather_api(location)
            message['Api_response'] = Api_response

        # call google translate api
        elif processor_port == input_ports["translate"]:
            string = message['Payload']
            Api_response = translate_api(string)
            message['Api_response'] = Api_response

        # call string_reverse api
        elif processor_port == input_ports["reverse"]:
            string = message['Payload']
            Api_response = translate_api(string)
            message['Api_response'] = Api_response

        elif processor_port == input_ports["c2c"]:  # client to client API
            client_message = message['Payload']  # check if client is active
            message['Api_response'] = client_message
        else:
            print("check input port")
        msg = json.dumps(message)  # sending message to dispatcher
        conn_2ia.send("free")
        conn_2dp.send(msg)

conn_2dp.close()
listener.close()
