
from urllib import response
from flask import Blueprint, render_template, request
import requests
API_KEY = "a709e0c27e22c8f1954335d792ddfda9"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather" 

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def base():
    if request.method == "POST":
        searchLocation = request.form.get('searchTerm')
        request_url = f"{BASE_URL}?appid={API_KEY}&q={searchLocation}"
        response = requests.get(request_url)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print("Error");

    return render_template("base.html")