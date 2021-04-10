from multiprocessing.connection import Listener, Client
import json
import sys
from rapidapi import str_rev_api, translate_api, weather_api, insta_api
input_ports={
    "instagram":8001,
    "weather":8002,
    "translate":8003,
    "reverse":8004,
    "c2c":8005
}

processor_port = int(sys.argv[1])
dispatcher_port = int(sys.argv[2])
listener = Listener(('locahost', processor_port), authkey=b'secret password')
conn_2dp = Client(('localhost', dispatcher_port), authkey=b'secret password')
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
        if processor_port==input_ports["instagram"]:  #call instagram api
            username = d['Payload']
            Api_response = insta_api(username)
            d['Api_response'] = Api_response
            

        elif processor_port==input_ports["weather"]: #call weather api
            location = d['Payload']
            Api_response = weather_api(location)
            d['Api_response'] = Api_response
            

        elif processor_port==input_ports["translate"]: #call google translate api
            string = d['Payload']
            Api_response = translate_api(string)
            d['Api_response'] = Api_response
            

        elif processor_port==input_ports["reverse"]:  #call string_reverse api
            string = d['Payload']
            Api_response = translate_api(string)
            d['Api_response'] = Api_response
            

        elif processor_port==input_ports["c2c"]:  #client to client API
            client_message = d['Payload'] #check if client is active
            d['Api_response'] = client_message
        else:
            print("check input port")
        
            
        msg = json.dumps(d)  #sending message to dispatcher
        conn_2dp.send(msg)  # is api_reponse a json object
        
conn_2dp.close()
listener.close()
