
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Find AgriNova main folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load API key from .env
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("WEATHER_API_KEY")

# API URLs
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


# Function 1: Get current weather
def get_weather(city):

    if not API_KEY:
        raise ValueError("Weather API key not found.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(
        CURRENT_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"].title(),
        "wind_speed": data["wind"]["speed"],
        "rainfall": data.get("rain", {}).get("1h", 0)
    }

    return weather_info


# Function 2: Get 5-day forecast
def get_forecast(city):

    if not API_KEY:
        raise ValueError("Weather API key not found.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    forecast = []

    # Select one forecast entry per day
    for item in data["list"]:

        if "12:00:00" in item["dt_txt"]:

            forecast.append({
                "date": item["dt_txt"].split(" ")[0],
                "temperature": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "condition": item["weather"][0]["description"].title()
            })

    return forecast
