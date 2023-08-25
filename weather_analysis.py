import os
import pytz
import pyowm
from pyowm.owm import OWM
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# API_KEY = os.environ['API_KEY']
owm = pyowm.OWM('f2894123f53cc162e5772bc4a05eeb08')
mgr=owm.weather_manager()

degree_sign=u'\N{DEGREE SIGN}'

st.title("5-Day Weather Forecast")
st.write("## Made by Anh Ha")
st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")
place=st.text_input("NAME OF THE CITY: ", "")

if place == None:
    st.write("Input a CITY!")

unit=st.selectbox("Select Temperature Unit", ("Celsius","Fahrenheit"))

g_type=st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

if unit=='Celsius':
    unit_c = 'celsius'
else:
    unit_c = 'fahrenheit'

def get_temperature():
    days = []
    dates = []
    temp_min = []
    temp_max = []
    #Forcaster provides a high level interface to the forecast so you can check whether or not there are
    #specific weather conditions (such as rain or clouds) in the forecast
    forecaster = mgr.forecast_at_place(place, '3h')

    #Forecast class gives you access to the actual values in the forecast, such as the
    #temperature, amount of rainfall
    forecast=forecaster.forecast

    for weather in forecast:
        day=datetime.utcfromtimestamp(weather.reference_time())
        date=day.date()
        if date not in dates:
            dates.append(date)
            temp_max.append(None)
            temp_min.append(None)
            days.append(date)
        temperature = weather.temperature(unit_c)['temp']
        if not temp_min[-1] or temperature < temp_min[-1]:
            temp_min[-1]=temperature
        if not temp_max[-1] or temperature > temp_max[-1]:
            temp_max[-1]=temperature
    return days, temp_min, temp_max

def init_plot():
    plt.figure('PyOWM', figsize=(10, 10))
    plt.xlabel('Day')
    plt.ylabel(f'Temperature ({degree_sign}F)')
    plt.title('Weekly Forcast')

def plot_temperatures(days, temp_min, temp_max):
    fig = go.Figure(
        data=[
            go.Bar(name='minimum temperature', x=days, y=temp_min),
            go.Bar(name='maximum temperature', x=days, y=temp_max)
        ]
    )
    fig.update_layout(barmode='group')
    return fig

def plot_temperatures_line(days, temp_min, temp_max):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=temp_min, name='minimum temperature'))
    fig.add_trace(go.Scatter(x=days, y=temp_max, name='maximum temperature'))
    return fig

def label_xaxis(days):
    plt.xticks(days)
    axes = plt.gca()
    xaxis_format=dates.DateFormatter('%d/%m')
    return axes.xaxis.set_major_formatter(xaxis_format)

def draw_bar_chart():
    days,temp_min,temp_max = get_temperature()
    st.title("Temperature Bar Chart")
    print("Temperature Bar Chart")
    fig = plot_temperatures(days, temp_min, temp_max)
    plot1 = st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperature")
    for i in range(0,5):
         st.write("### ", temp_min[i],degree_sign,' --- ',temp_max[i],degree_sign)

def draw_line_chart():
    days,temp_min,temp_max = get_temperature()
    st.title("Temperature Line Chart")
    print("Temperature Line Chart")
    fig = plot_temperatures_line(days, temp_min, temp_max)
    plot2 = st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperature")
    print("Minimum and Maximum Temperature")
    for i in range(0,5):
        st.write("### ", temp_min[i],degree_sign, " --- ", temp_max[i],degree_sign)

def min_and_max_temp():
    days,temp_min,temp_max = get_temperature()
    st.title("Minimum and Maximum Temperature")
    for i in range(0,5):
        st.write("### ", temp_min[i],degree_sign, " --- ", temp_max[i],degree_sign)

def other_weather_updates():
    forecaster = mgr.forecast_at_place(place, '3h')
    st.title('Impending Temperature Changes: ')
    if forecaster.will_have_fog():
        st.write("### Fog Alert!")
    if forecaster.will_have_rain():
        st.write(" ### Rain Alert!")
    if forecaster.will_have_storm():
        st.write(" ### Storm Alert")
    if forecaster.will_have_snow():
        st.write(" ### Snow Alert!")
    if forecaster.will_have_tornado():
        st.write(" ### Tornado Alert!")
    if forecaster.will_have_hurricane():
        st.write(" ### Hurricane Alert!")
    if forecaster.will_have_clouds():
        st.write(" ### Cloudy Skies")
    if forecaster.will_have_clear():
        st.write(" ### Clear Weather!")


def cloud_and_wind():
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    cloud_cov = weather.clouds
    winds=weather.wind()['speed']
    st.title("Cloud coverage and wind speed")
    st.write(" ### The current cloud coverage for", place, "is", cloud_cov, "%")
    st.write(' ### The current wind speed for',place, 'is', winds, 'mph')


def sunrise_and_sunset():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    st.title('Sunrise and sunset time: ')
    finland = pytz.timezone("Europe/Helsinki")
    sunset = weather.sunset_time(timeformat = "iso")
    sunrise = weather.sunrise_time(timeformat = "iso")
    st.write(" ### Sunrise time in", place, "is", sunrise)
    st.write(" ### Sunset time in", place, "is", sunset)

def sunrise_and_sunset_test():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    st.title('Sunrise and sunset time: ')
    finland = pytz.timezone("Europe/Helsinki")
    ss = weather.sunset_time(timeformat = "iso")
    sr = weather.sunrise_time(timeformat = "iso")
    st.write(" ### Sunrise time in", place, "is", sr)
    st.write(" ### Sunset time in", place, "is", ss)

def updates():
    other_weather_updates()
    cloud_and_wind()
    sunrise_and_sunset()

if __name__ == '__main__':
    # if st.button("SUBMIT"):
    #     draw_line_chart()
    #     draw_bar_chart()
    #     updates()

    if st.button("SUBMIT"):
        if g_type == 'Line Graph':
            draw_line_chart()
        else:
            draw_bar_chart()
        updates()