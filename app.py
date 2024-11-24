from flask import Flask, render_template, request
import requests

nasa_api_key = "hxLOCDifqXUEkScloiqppBB5iYg7eE4Q7MBWh7r6"

apod_api_url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&count=5"
apod_title_image_url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&count=1"
neo_url = f"https://api.nasa.gov/neo/rest/v1/feed?&api_key={nasa_api_key}"
CME_url = f"https://api.nasa.gov/DONKI/CMEAnalysis?&mostAccurateOnly=true&speed=500&halfAngle=30&catalog=ALL&api_key={nasa_api_key}"
mars_rover_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={nasa_api_key}"


app = Flask(__name__)

def apod_info():
    response = requests.get(apod_api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error :Something is broken"}

def title_image():
    response = requests.get(apod_title_image_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"No title image for today because I messed up something"}

def neos():
    neo_response = requests.get(neo_url)
    if neo_response.status_code == 200:
        return neo_response.json().get("near_earth_objects", {})
    else:
        return {"error: No NEO objects safe or not?"}

def space_weather_data():
    space_weather_response = requests.get(CME_url)
    if space_weather_response.status_code == 200:
        return space_weather_response.json()
    else:
        return {"error: Could not fetch space weather data"}

def mars_data():
    mars_response = requests.get(mars_rover_url)
    if mars_response.status_code == 200:
        data = mars_response.json()
        return data.get("latest_photos", [])
    else:
        return {"error: while fetching data from nasa mars api"}

@app.route("/")
def index():
    response_value = apod_info()
    title_image_ = title_image()
    neos_r = neos()
    return render_template("index.html", response_value=response_value, title_image=title_image_, neos_r=neos_r)

@app.route("/space_weather")
def space_weather():
    space_data_ = space_weather_data()
    return render_template("space_weather.html", data=space_data_)

@app.route("/mars_pic")
def mars_updates():
    mars_data_ = mars_data()
    return render_template("mars_pic.html", photo_data = mars_data)


if __name__ == "__main__":
    app.run(debug=True)
