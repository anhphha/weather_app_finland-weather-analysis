# weather_app_finland-weather-analysis
A web application to display weather updates

## Features

- 5 day weather forecast
- Impending Weather changes
- Weather Graph
- Sunrise and sunset times
- CLoud Coverage
- Wind Speed

## Built Using

- Python
- Streamlit
- Plotly
- Python Open Weather Map API

## :fire: Proof of Concept - Demo Link

https://weather-analysis-finland.herokuapp.com

## :bulb: Helpful commands:
- `source ENV/bin/activate`
- `python3 -m venv env`
- `pip install flask requests python-dotenv`
- `pip list`
- `pip freeze > requirements.txt`

### Heroku commands:
- `heroku login`
- `heroku create weather-analysis-finland`
- `heroku config:set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python --app weather-analysis-finland`
- `heroku config:set BUILDPACK_URL=https://github.com/andrewychoi/heroku-buildpack-scipy.git `
- `git add`
- `git commit -m`
- `heroku stack:set heroku-20`
- `git push heroku main`
- `heroku open`
- `heroku ps:scale web=1`
- `heroku restart`
- `heroku logs --tail`


