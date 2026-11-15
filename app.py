
import os
import pickle
import pandas as pd
import requests

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from src.soil_analysis import analyze_soil
from src.weather import get_weather, get_forecast
from src.knowledge_hub import get_all_crops, get_crop_details
from src.disease_prediction import predict_disease
from src.disease_info import get_disease_details, get_display_name


# CREATE FLASK APPLICATION
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path, "static", "uploads"
)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


# LOAD CROP RECOMMENDATION MODEL
with open(
    os.path.join(app.root_path, "models", "crop_model.pkl"), "rb"
) as file:
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
                weather = get_weather(city)
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


# MODULE 4: PLANT DISEASE DETECTION

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/plant-disease", methods=["GET", "POST"])
def plant_disease():

    prediction = None
    confidence = None
    error = None
    image_path = None
    symptoms = None
    care = None
    prevention = None

    if request.method == "POST":

        if "leaf_image" not in request.files:
            error = "Please upload a leaf image."

        else:
            file = request.files["leaf_image"]

            if file.filename == "":
                error = "No image selected."

            elif not allowed_file(file.filename):
                error = "Only JPG, JPEG and PNG images are allowed."

            else:
                try:
                    filename = secure_filename(file.filename)

                    save_path = os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )

                    file.save(save_path)

                    image_path = "/static/uploads/" + filename

                    # PREDICT DISEASE
                    raw_prediction, confidence = predict_disease(save_path)

                    # GET DISEASE INFORMATION
                    info = get_disease_details(raw_prediction)

                    prediction = get_display_name(raw_prediction)

                    if info is not None:

                        symptoms = info["symptoms"]
                        care = info["care"]
                        prevention = info["prevention"]

                    elif raw_prediction.endswith("___healthy"):

                        symptoms = "No visible disease detected by the model."

                        care = (
                            "Continue regular watering, provide suitable "
                            "sunlight and monitor plant growth."
                        )

                        prevention = (
                            "Maintain proper spacing, healthy soil "
                            "and regular plant inspection."
                        )

                    else:

                        symptoms = (
                            "Detailed symptoms information is not available yet."
                        )

                        care = (
                            "Consult a local agricultural expert for "
                            "disease-specific guidance."
                        )

                        prevention = (
                            "Use healthy planting material and monitor "
                            "the plant regularly."
                        )

                    if confidence < 60:
                        error = (
                            "Low confidence prediction. Please upload "
                            "a clearer leaf image and do not rely on "
                            "this result alone."
                        )

                except Exception as e:
                    error = "Prediction failed: " + str(e)

    return render_template(
        "plant_disease.html",
        prediction=prediction,
        confidence=confidence,
        image_path=image_path,
        symptoms=symptoms,
        care=care,
        prevention=prevention,
        error=error
    )


# MODULE 5: FARMING KNOWLEDGE HUB

@app.route("/knowledge-hub", methods=["GET", "POST"])
def knowledge_hub():

    crops = get_all_crops()
    selected_crop = None
    details = None

    if request.method == "POST":

        selected_crop = request.form.get("crop")
        details = get_crop_details(selected_crop)

    return render_template(
        "knowledge_hub.html",
        crops=crops,
        selected_crop=selected_crop,
        details=details
    )


# RUN FLASK APPLICATION

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
