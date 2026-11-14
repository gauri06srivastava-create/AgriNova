import os
from werkzeug.utils import secure_filename
from src.disease_prediction import predict_disease
from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests
from src.soil_analysis import analyze_soil
from src.weather import get_weather, get_forecast
from src.knowledge_hub import get_all_crops, get_crop_details


# Create Flask application
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
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


# MODULE 4: PLANT DISEASE DETECTION

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

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

@app.route("/plant-disease", methods=["GET", "POST"])
def plant_disease():

    prediction = None
    confidence = None
    error = None
    image_path = None
    symptoms = None
    care = None

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

                    prediction, confidence = predict_disease(save_path)

                    image_path = "/" + save_path.replace("\\", "/")

                    if confidence < 60:
                        error = (
                            "Low confidence prediction. "
                            "Please upload a clearer leaf image "
                            "and do not rely on this result alone."
                        )

                    disease_info = {
                        "Grape___Black_rot": {
                            "symptoms": "Dark brown or black spots on leaves and berries.",
                            "care": "Remove infected plant parts, maintain airflow "
                                    "and avoid overhead watering."
                        }
                    }

                    info = disease_info.get(prediction)

                    if info:
                        symptoms = info["symptoms"]
                        care = info["care"]

                except Exception as e:
                    error = "Prediction failed: " + str(e)

    return render_template(
        "plant_disease.html",
        prediction=prediction,
        confidence=confidence,
        image_path=image_path,
        symptoms=symptoms,
        care=care,
        error=error
    )

# Run Flask application
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
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