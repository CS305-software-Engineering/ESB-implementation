# helping libraries
import http.client

# method that interacts with string reverse API
# input : a string that needs to be reversed
def str_rev_api(string):
    # setup connection
    conn = http.client.HTTPSConnection("sonigarima.pythonanywhere.com")
    # prepare the input as accepted by API
    ip = "/" + str(string)
    # request the output
    conn.request("GET", ip)
    # Store the response and read it
    res = conn.getresponse()
    data = res.read()
    # return the response
    return data.decode("utf-8")

#current weather data
# input : city name
def weather_api(city):
    # setup connection
    conn = http.client.HTTPSConnection("community-open-weather-map.p.rapidapi.com")
    # RAPIDAPI CREDENTIALS
    headers = {
        'x-rapidapi-key': "48a9d3acbemsh51e3d6835ad11bep1a253cjsne66f78646111",
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }
    # prepare the input as accepted by API
    ip = "/weather?q=" + str(city) + "%2Cuk&lat=0&lon=0&callback=test&id=2172797&lang=null&units=%22metric%22%20or%20%22imperial%22&mode=xml%2C%20html"
    # request the output
    conn.request("GET", ip, headers=headers)
    # Store the response and read it
    res = conn.getresponse()
    data = res.read()
    # status of request
    status=res.status
    # return the response
    return data.decode("utf-8")


#instagram account info
def insta_api(username):
    # setup connection
    conn = http.client.HTTPSConnection("instagram40.p.rapidapi.com")
    # RAPIDAPI CREDENTIALS
    headers = {
        'x-rapidapi-key': "48a9d3acbemsh51e3d6835ad11bep1a253cjsne66f78646111",
        'x-rapidapi-host': "instagram40.p.rapidapi.com"
    }
    # prepare the input as accepted by API
    ip = "/account-info?username=" + str(username)
    # request the output
    conn.request("GET", ip, headers=headers)
    # Store the response and read it
    res = conn.getresponse()
    data = res.read()
    # status of request
    status=res.status
    # return the response
    return data.decode("utf-8")


#detect language
def translate_api(payload):
    # setup connection
    conn = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")
    # RAPIDAPI CREDENTIALS
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept-encoding': "application/gzip",
        'x-rapidapi-key': "48a9d3acbemsh51e3d6835ad11bep1a253cjsne66f78646111",
        'x-rapidapi-host': "google-translate1.p.rapidapi.com"
    }
    # prepare the input as accepted by API
    payload_final = "q=" + str(payload)
    # request the output
    conn.request("POST", "/language/translate/v2/detect", payload_final,headers)
    # Store the response and read it
    res = conn.getresponse()
    data = res.read()
    # status of request
    status=res.status
    # return the response
    return data.decode("utf-8")


input = "nishith.jupally"


out=insta_api(input)

