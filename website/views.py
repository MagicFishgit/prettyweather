from unittest import case
from urllib import response
from flask import Blueprint, render_template, request
import requests
from creds import openweather_api_key
import datetime

API_KEY = openweather_api_key
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"
LOCATION_URL = "http://api.openweathermap.org/geo/1.0/direct"
POLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution" 

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def base():
    if request.method == "POST":
        search_location = request.form.get('searchTerm')
        data_lon = None
        data_lat = None
        exclude = "minute,hourly"
        location_request_url = f"{LOCATION_URL}?q={search_location}&limit=1&appid={API_KEY}"

        #Get coordinates for onecall API
        response = requests.get(location_request_url)

        if response.status_code == 200:
            data = response.json()
            data_lat = data[0]['lat']
            data_lon = data[0]['lon']

            onecall_request_url = f"{BASE_URL}?lat={data_lat}&lon={data_lon}&exclude={exclude}&appid={API_KEY}"

            #Make onecall API call with location data
            response = requests.get(onecall_request_url)

            if response.status_code == 200:
                data = response.json()

                #Get current data
                curr_weather = Weather(data, "current")

                #Get daily forecast data
                forecast = []
                for d in data['daily']:
                    forecast.append(Weather(d, "daily"))

            else:
                print(response.status_code)
                print(response.reason)

            #Get pollution data.
            pollution_request_url = f"{POLLUTION_URL}?lat={data_lat}&lon={data_lon}&appid={API_KEY}"
            
            #Make pollution api call with location data.
            response = requests.get(pollution_request_url)

            if response.status_code == 200:
                data = response.json()

                #Parse pollution data
                pollution_data = Pollution(data)

            else:
                print(response.status_code)
                print(response.reason)
                
            return render_template("base.html",longitude = data_lon, latitude = data_lat, curr_weather = curr_weather, forecast = forecast, location_name = search_location, poll_data = pollution_data)
        else:
            print(response.status_code)
            print(response.reason)

    #If not loading by POST supply default lat long. -33.95623812649303, 18.617579341316596
    lon = "18.61"
    lat = "-33.95"
    return render_template("base.html",longitude=18.61, latitude=-33.95)

class Weather:

    def __init__(self, weather_dict, period):
        self.period = period
        
        if period == "current":
            self.date = Date(weather_dict[period].get("dt"))
            self.sunrise = Date(weather_dict[period]['sunrise'])
            self.sunset = Date(weather_dict[period]['sunset'])
            self.temp = round(weather_dict[period]['temp'] - 273.15, 1)
            self.feels_like = round(weather_dict[period]['feels_like'] - 273.15, 1)
            self.pressure = weather_dict[period]['pressure']
            self.humidity = weather_dict[period]['humidity']
            self.clouds = weather_dict[period]['clouds']
            self.uvi = weather_dict[period]['uvi']
            self.wind_speed = weather_dict[period]['wind_speed']
            self.wind_deg = weather_dict[period]['wind_deg']
            self.weather_main = weather_dict[period]['weather'][0].get("main")
            self.weather_desc = weather_dict[period]['weather'][0].get("description")
            self.weather_icon = get_icon(self.weather_main)
        else:
            self.date = Date(weather_dict['dt'])
            self.sunrise = Date(weather_dict['sunrise'])
            self.sunset = Date(weather_dict['sunset'])
            self.temp = round(weather_dict['temp'].get("day") - 273.15, 1)
            self.temp_min = round(weather_dict['temp'].get("min") - 273.15, 1)
            self.temp_max = round(weather_dict['temp'].get("max") - 273.15, 1)
            self.feels_like = round(weather_dict['feels_like'].get("day") - 273.15, 1)
            self.pressure = weather_dict['pressure']
            self.humidity = weather_dict['humidity']
            self.clouds = weather_dict['clouds']
            self.uvi = weather_dict['uvi']
            self.wind_speed = weather_dict['wind_speed']
            self.wind_deg = weather_dict['wind_deg']
            self.weather_main = weather_dict['weather'][0].get("main")
            self.weather_desc = weather_dict['weather'][0].get("description")
            self.weather_icon = get_icon(self.weather_main)
            

class Date:

    def __init__(self, utc_stamp):

        self.datetime_obj = datetime.datetime.fromtimestamp(utc_stamp)
        self.day = self.datetime_obj.day
        self.month = self.datetime_obj.month
        self.month_name = self.get_month_name(self.month)
        self.year = self.datetime_obj.year
        self.hour = self.datetime_obj.hour
        self.minute = self.datetime_obj.minute

class Pollution:
    def __init__(self, data):

        self.aqi = data['list'][0]['main'].get('aqi') #Air Quality Index 1-5
        self.aqi_desc = self.get_air_quality(self.aqi)
        self.co = data['components'].get('co') #Carbon Monoxide
        self.no = data['components'].get('no') #Nitrogen Dioxide
        self.pm2_5 = data['components'].get('pm2_5') # Fine Particles matter
        self.pm10 = data['components'].get('pm10') #Coarse particulate matter
    
    def get_air_quality(aqi):
        if aqi == 1:
            aqi_desc = "good"
        elif aqi == 2:
            aqi_desc = "Fair"
        elif aqi == 3:
            aqi_desc = "moderate"
        elif aqi == 4:
            aqi_desc = "poor"
        else:
            aqi_desc = "very poor"
    
    def get_month_name(self, month):
        
        if month == 1:
            return "Jan"
        elif month == 2:
            return "Feb"
        elif month == 3:
            return "Mar"
        elif month == 4:
            return "Apr"
        elif month == 5:
            return "May"
        elif month == 6:
            return "Jun"
        elif month == 7:
            return "Jul"
        elif month == 8:
            return "Aug"
        elif month == 9:
            return "Sep"
        elif month == 10:
            return "Oct"
        elif month == 11:
            return "Nov"
        else: return "Dec"

def get_icon(weather_main):
    
    #Determine weather icon. For some reason python won't set the Clear condition value even if it is true but everything else it will.
    weather_icon = "fa-sun"

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