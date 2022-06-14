import requests
from flask import Flask, render_template
import os
from weather_app import sunrise_and_sunset_test
from weather_app import sunrise_and_sunset
from weather_app import updates
from weather_app import cloud_and_wind
from weather_app import other_weather_updates
from weather_app import min_and_max_temp
from weather_app import get_temperature
from weather_app import draw_line_chart
from weather_app import draw_bar_chart
from weather_app import plot_temperatures_line
from weather_app import plot_temperatures
from weather_app import label_xaxis
from weather_app import init_plot

API_KEY = os.environ["API_KEY"]
BASE_URL = os.environ.get("BASE_URL")
user_input = "helsinki"
LAT = 60.1699
LON = 24.9384

application=Flask(__name__, static_url_path="",
                  static_folder="web/static", template_folder="web/templates")

@application.route('/')

def hello_world():
    # r = requests.get(
    #         f'{BASE_URL}/weather?q={user_input}&units=metrics&appid={API_KEY}')
    #     r.raise_for_status()
    #     data = r.json()

    weather1 = sunrise_and_sunset('Helsinki')
    weather2 = cloud_and_wind('Helsinki')
    weather3 = other_weather_updates("Helsinki")
    weather4 = min_and_max_temp("Helsinki")
    weather5 = draw_line_chart("Helsinki")
    weather6 = draw_bar_chart("Helsinki")
    return render_template('index.html', homepage=(weather1, weather2, weather3, weather4, weather5, weather6))


@application.route('/test')

def hello_world_test():
    updated_weather = updates("Helsinki")
    return  render_template('index.html', message=updated_weather)

@application.route('/current')
def current():
    try:
        r = requests.get(
            f'{BASE_URL}/weather?q={user_input}&units=metrics&appid={API_KEY}')
        r.raise_for_status()
        data = r.json()

        current_weather = {
            "description" : data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "name": data["name"],
            "temperature": round(data["main"]["temp"] -273.15),
            "wind": data["wind"]["speed"]
        }

        return render_template("index.html", weather=current_weather)
    except requests.exceptions.HTTPError as err:
        return f"Error: {err}"

@application.route('/forecast')

def forecast():
    r = requests.get(f'{BASE_URL}/onecall?lat={LAT}&lon={LON}&units=metrics&appid={API_KEY}').json()
    return render_template("index.html", forecast= r["daily"])

@application.errorhandler(404)

def page_not_found(error):
    return render_template("index.html", message=error), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(debug =  True, host="0.0.0.0", port = port)
