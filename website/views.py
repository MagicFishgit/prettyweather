
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
            weather_main = data['weather'][0]['main']
            temperature = round(data['main']['temp'] - 273.15)
            feels_like = round(data['main']['feels_like'] - 273.15)
            temp_min = round(data['main']['temp_min'] - 273.15)
            temp_max = round(data['main']['temp_max'] - 273.15)
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            visibility = data['visibility']
            wind_speed = data['wind']['speed']
            cloud_percentage = data['clouds']['all']
            country = data['sys']['country']
            city = data['name']
            lon = data['coord']['lon']
            lat = data['coord']['lat']

            #Determine weather icon
            weather_icon = None

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

            print(data)
            print(lon)
            print(lat)

            return render_template("base.html",longitude=lon, latitude=lat, city_name=city, temp=temperature, min_temp=temp_min, max_temp=temp_max, fa_icon=weather_icon, weather_desc= weather)
        else:
            print("Error");

    #If not loading by POST supply default lat long. -33.95623812649303, 18.617579341316596
    lon = "18.61"
    lat = "-33.95"
    return render_template("base.html",longitude=lon, latitude=lat)