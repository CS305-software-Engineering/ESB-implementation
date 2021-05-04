# helping libraries
import http.client
from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
INSTA_API_KEY = os.getenv('INSTA_API_KEY')
TRANSLATE_API_KEY = os.getenv('TRANSLATE_API_KEY')


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
    conn = http.client.HTTPSConnection(
        "community-open-weather-map.p.rapidapi.com")
    # RAPIDAPI CREDENTIALS
    headers = {
        'x-rapidapi-key': str(WEATHER_API_KEY),
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }
    # prepare the input as accepted by API
    ip = "/weather?q=" + str(
        city
    ) + "%2C&lat=0&lon=0&callback=test&id=2172797&lang=null&units=%22metric%22%20or%20%22imperial%22&mode=xml%2C%20html"
    # request the output
    conn.request("GET", ip, headers=headers)
    # Store the response and read it
    res = conn.getresponse()
    data = res.read()
    # status of request
    status = res.status
    # return the response
    return data.decode("utf-8")


#instagram account info
def insta_api(username):
    # setup connection
    conn = http.client.HTTPSConnection("instagram40.p.rapidapi.com")
    # RAPIDAPI CREDENTIALS
    headers = {
        'x-rapidapi-key': str(INSTA_API_KEY),
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
    status = res.status
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
        'x-rapidapi-key': str(TRANSLATE_API_KEY),
        'x-rapidapi-host': "google-translate1.p.rapidapi.com"
    }
    # prepare the input as accepted by API
    payload_final = "q=" + str(payload)
    # request the output
    conn.request("POST", "/language/translate/v2/detect", payload_final,
                 headers)
    # Store the response and read it
    res = conn.getresponse()
    data = res.read()
    # status of request
    status = res.status
    # return the response
    return data.decode("utf-8")
