
from urllib import response
from flask import Blueprint, render_template, request
import requests
from creds import openweather_api_key

API_KEY = openweather_api_key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather" 

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def base():
    if request.method == "POST":
        search_location = request.form.get('searchTerm')
        request_url = f"{BASE_URL}?appid={API_KEY}&q={search_location}"
        response = requests.get(request_url)

        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = round(data['main']['temp'] - 273.15)
            feels_like = round(data['main']['feels_like'] - 273.15)
            temp_min = round(data['main']['temp_min'] - 273.15)
            temp_max = round(data['main']['temp_min'] - 273.15)
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            visibility = data['visibility']
            wind_speed = data['wind']['speed']
            cloud_percentage = data['clouds']['all']
            country = data['sys']['country']
            city = data['name']
            lon = data['coord']['lon']
            lat = data['coord']['lat']

            print(data)
            print(lon)
            print(lat)

            return render_template("base.html",longitude=lon, latitude=lat)
        else:
            print("Error");

    #If not loading by POST supply default lat long. -33.95623812649303, 18.617579341316596
    lon = "18.61"
    lat = "-33.95"
    return render_template("base.html",longitude=lon, latitude=lat)