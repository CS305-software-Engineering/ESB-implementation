from multiprocessing.connection import Listener, Client
from socket import *
import json
import sys
import time
from rapidapi import str_rev_api, translate_api, weather_api, insta_api

time.sleep(2)
input_ports = {
    "instagram": 8001,
    "weather": 8002,
    "translate": 8003,
    "reverse": 8004,
    "C2C": 8005
}

processor_port = int(sys.argv[1])
dispatcher_port = int(sys.argv[2])
listener = Listener(('localhost', processor_port), authkey=b'secret password')
conn_2dp = Client(('localhost', dispatcher_port), authkey=b'secret password')
running = True
conn_2ia = listener.accept()

print('in proc_mod connection accepted from', listener.last_accepted,
      processor_port)

while running:
    msg = conn_2ia.recv()
    if msg == 'terminate':
        print(f"terminate processing module {processor_port}")
        conn_2dp.send('terminate')
        conn_2ia.close()
        running = False
    else:
        # print("data received for processing")
        # process api
        # create client to seng to dispacter
        # close the client connection
        # close this connection
        #message = json.loads(msg)
        message = msg
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
            Api_response = str_rev_api(string)
            message['Api_response'] = Api_response

        elif processor_port == input_ports["C2C"]:  # client to client API
            client_message = message['Payload']  # check if client is active
            message['Api_response'] = client_message
        else:
            print("check input port")
        msg = json.dumps(message)  # sending message to dispatcher
        conn_2ia.send("free")
        conn_2dp.send(msg)

conn_2dp.close()
listener.close()
