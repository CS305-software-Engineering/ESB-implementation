import http.client

index=3

#current weather data

if(index==1):
    conn = http.client.HTTPSConnection("community-open-weather-map.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "48a9d3acbemsh51e3d6835ad11bep1a253cjsne66f78646111",
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

    conn.request("GET", "/weather?q=Warangal&lat=0&lon=0&callback=test&id=2172797&lang=null&units=%22metric%22%20or%20%22imperial%22&mode=xml%2C%20html", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


#instagram account info
if(index==2):
    conn = http.client.HTTPSConnection("instagram40.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "48a9d3acbemsh51e3d6835ad11bep1a253cjsne66f78646111",
        'x-rapidapi-host': "instagram40.p.rapidapi.com"
        }

    conn.request("GET", "/account-info?username=sathwiik_reddy_", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

#detect language
if(index==3):
    conn = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")

    payload = "q=English%20is%20hard%2C%20but%20detectably%20so"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept-encoding': "application/gzip",
        'x-rapidapi-key': "48a9d3acbemsh51e3d6835ad11bep1a253cjsne66f78646111",
        'x-rapidapi-host': "google-translate1.p.rapidapi.com"
        }

    conn.request("POST", "/language/translate/v2/detect", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
