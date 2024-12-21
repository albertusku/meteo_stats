from datetime import datetime
import os

#PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'Data_storage','Storage')
API_DIR = os.path.join(BASE_DIR, 'API')
HISTORICAL_WEATHER_DIR=os.path.join(DATA_DIR, 'Historical_weather.xlsx')
HISTORICAL_WEATHER_FORECAST_DIR=os.path.join(DATA_DIR, 'Historical_weather_forecast.xlsx')
STADISTICS_DAY_DIR=os.path.join(DATA_DIR, 'Stadistics_day.xlsx')
STADISTICS_MONTH_DIR=os.path.join(DATA_DIR, 'Stadistics_month.xlsx')
WEATHER_API_DIR=os.path.join(API_DIR,'api_weather_response.json')
TOMORROW_API_DIR=os.path.join(API_DIR,'api_tomorrow_response.json')
TOMORROW_API_FORECAST_DIR=os.path.join(API_DIR,'api_tomorrow_forecast_response.json')

#DATETIME
now=datetime.now()

#URLS
weather_api_url = "https://api.openweathermap.org/data/2.5/weather"
tomorrow_api_url= url = "https://api.tomorrow.io/v4/weather/forecast"