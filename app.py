
from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests
from src.soil_analysis import analyze_soil
from src.weather import get_weather, get_forecast


# Create Flask application
app = Flask(__name__)


# Load trained crop recommendation model
with open("models/crop_model.pkl", "rb") as file:
    model = pickle.load(file)


# MODULE 1: CROP RECOMMENDATION
@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    error = None

    if request.method == "POST":

        try:
            N = float(request.form["N"])
            P = float(request.form["P"])
            K = float(request.form["K"])

            temperature = float(request.form["temperature"])
            humidity = float(request.form["humidity"])
            ph = float(request.form["ph"])
            rainfall = float(request.form["rainfall"])

            if N < 0 or P < 0 or K < 0:
                raise ValueError("NPK values cannot be negative.")

            if not 0 <= humidity <= 100:
                raise ValueError("Humidity must be between 0 and 100.")

            if not 0 <= ph <= 14:
                raise ValueError("Soil pH must be between 0 and 14.")

            if rainfall < 0:
                raise ValueError("Rainfall cannot be negative.")

            user_data = pd.DataFrame(
                [[N, P, K, temperature, humidity, ph, rainfall]],
                columns=[
                    "N", "P", "K",
                    "temperature", "humidity",
                    "ph", "rainfall"
                ]
            )

            prediction = model.predict(user_data)[0]

        except ValueError as e:
            error = str(e)

        except Exception as e:
            error = "Something went wrong: " + str(e)

    return render_template(
        "index.html",
        prediction=prediction,
        error=error
    )


# MODULE 2: SOIL ANALYSIS
@app.route("/soil-analysis", methods=["GET", "POST"])
def soil_analysis():

    result = None
    error = None

    if request.method == "POST":

        try:
            N = float(request.form["N"])
            P = float(request.form["P"])
            K = float(request.form["K"])
            ph = float(request.form["ph"])

            result = analyze_soil(N, P, K, ph)

        except ValueError as e:
            error = str(e)

        except Exception as e:
            error = "Something went wrong: " + str(e)

    return render_template(
        "soil_analysis.html",
        result=result,
        error=error
    )


# MODULE 3: WEATHER INFORMATION
@app.route("/weather", methods=["GET", "POST"])
def weather_page():

    weather = None
    forecast = None
    error = None

    if request.method == "POST":

        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."

        else:
            try:
                # Get current weather
                weather = get_weather(city)

                # Get 5-day forecast
                forecast = get_forecast(city)

            except requests.exceptions.RequestException:
                error = "Unable to fetch weather data. Please try again."

            except ValueError as e:
                error = str(e)

            except Exception as e:
                error = "Something went wrong: " + str(e)

    return render_template(
        "weather.html",
        weather=weather,
        forecast=forecast,
        error=error
    )


# Run Flask application
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
