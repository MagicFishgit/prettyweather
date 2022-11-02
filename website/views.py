from unittest import case
from urllib import response
from flask import Blueprint, render_template, request
import requests
from api import get_data

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def base():
    if request.method == "POST":
        search_location = request.form.get('searchTerm')
        longitude, latitude, curr_weather, forecast, poll_data = get_data(search_location)
                
        return render_template("base.html",longitude = longitude, latitude = latitude, curr_weather = curr_weather, forecast = forecast, location_name = search_location, poll_data = poll_data)
    else:
        print("Invalid location or an error has occured.")

    #If not loading by POST supply default values/objects
    #Default Cape Town, South Africa
    search_location = "cape town, south africa"
    longitude, latitude, curr_weather, forecast, poll_data = get_data(search_location)
    return render_template("base.html",longitude = longitude, latitude = latitude, curr_weather = curr_weather, forecast = forecast, location_name = search_location, poll_data = poll_data)

