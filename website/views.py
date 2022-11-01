from urllib import response
from flask import Blueprint, render_template, request
import requests
from creds import openweather_api_key

API_KEY = openweather_api_key
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"
LOCATION_URL = "http://api.openweathermap.org/geo/1.0/direct" 

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def base():
    if request.method == "POST":
        search_location = request.form.get('searchTerm')
        data_lon = None
        data_lat = None
        exclude = "minute,hourly"
        location_request_url = f"{LOCATION_URL}?q={search_location}&limit=1&appid={API_KEY}"
        onecall_request_url = f"{BASE_URL}?lat={data_lat}&lon={data_lon}&exclude={exclude}&appid={API_KEY}"

        #Get coordinates for onecall API
        response = requests.get(location_request_url)

        if response.status_code == 200:
            data = response.json()
            data_lon = data[0]['lon']
            data_lat = data[0]['lat']

            #Make onecall API call with location data
            response = requests.get(onecall_request_url)

            if response.status_code == 200:
                data = response.json()

                print(data)
            else:
                print(response.status_code)
                print(response.reason)
                
            print("TEST:")
            print(data_lon,data_lat)

            #Determine weather icon
            #weather_icon = get_icon(weather_main)

            return render_template("base.html",longitude=18.61, latitude=-33.95)
        else:
            print("Error")

    #If not loading by POST supply default lat long. -33.95623812649303, 18.617579341316596
    lon = "18.61"
    lat = "-33.95"
    return render_template("base.html",longitude=18.61, latitude=-33.95)

def parse_data(flag, data):

    #Extracted values
    parsed_data_dict = {
        "weather" : "",
        "weather_main" : "",
        "temp_curr" : "",
        "feels_like" : "",
        "temp_min" : "",
        "temp_max" : "",
        "pressure" : "",
        "humidity" : "",
        "visibility" : "",
        "wind_speed" : "",
        "cloud_percentage" : "",
        "country" : "",
        "city" : "",
        "lon" : "",
        "lat" : ""
    }
    
    #Flag = 0 for current data.
    #Flag = 1 for 5 day forecast.
    if flag == 0:
        pass
    elif flag == 1:
        pass

def get_icon(weather_check):
    
    #Determine weather icon
    weather_icon = None
    weather_main = weather_check

    if weather_main == "Clear":
        weather_icon == "fa-sun"
    elif weather_main == "Clouds":
        weather_icon = "fa-cloud"
    elif weather_main == "Thunderstorm":
        weather_icon = "fa-bolt"
    elif weather_main == "Drizzle":
        weather_icon = "fa-cloud-rain"
    elif weather_main == "Rain":
        weather_icon = "fa-cloud-showers-heavy"
    elif weather_main == "Snow":
        weather_icon = "fa-snow-flake"
    elif weather_main == "Mist":
        weather_icon = "fa-cloud-fog"
    elif weather_main == "Smoke":
        weather_icon = "fa-smoke"
    elif weather_main == "Haze":
        weather_icon = "fa-sun-haze"
    elif weather_main == "Dust":
        weather_icon = "fa-sun-dust"
    elif weather_main == "Fog":
        weather_icon = "fa-cloud-fog"
    elif weather_main == "Ash":
        weather_icon = "fa-fire-smoke"
    elif weather_main == "Squall":
        weather_icon = "fa-cloud-bolt-sun"
    else:
        weather_icon = "fa-tornado"
    
    return weather_icon