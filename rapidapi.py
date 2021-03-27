import http.client

index=3


def str_rev_api(string):
    conn = http.client.HTTPSConnection("sonigarima.pythonanywhere.com")
    ip = "/"+str(string)
    conn.request("GET", ip)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

#current weather data
def weather_api(city):
    conn = http.client.HTTPSConnection("community-open-weather-map.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "48a9d3acbemsh51e3d6835ad11bep1a253cjsne66f78646111",
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }
    ip = "/weather?q="+str(city)+"%2Cuk&lat=0&lon=0&callback=test&id=2172797&lang=null&units=%22metric%22%20or%20%22imperial%22&mode=xml%2C%20html"
    conn.request("GET", ip, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

#instagram account info
def  insta_api(username):
    conn = http.client.HTTPSConnection("instagram40.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "48a9d3acbemsh51e3d6835ad11bep1a253cjsne66f78646111",
        'x-rapidapi-host': "instagram40.p.rapidapi.com"
        }
    ip = "/account-info?username="+str(username)
    conn.request("GET", ip, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

#detect language
def translate_api(payload):
    conn = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept-encoding': "application/gzip",
        'x-rapidapi-key': "48a9d3acbemsh51e3d6835ad11bep1a253cjsne66f78646111",
        'x-rapidapi-host': "google-translate1.p.rapidapi.com"
        }
    payload_final = "q="+str(payload)
    conn.request("POST", "/language/translate/v2/detect", payload_final, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
