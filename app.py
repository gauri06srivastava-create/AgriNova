
from flask import Flask, render_template, request
import pickle
import pandas as pd

# Flask application
app = Flask(__name__)

# Load trained crop recommendation model
with open("models/crop_model.pkl", "rb") as file:
    model = pickle.load(file)


# Home page and crop prediction
@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    error = None

    if request.method == "POST":

        try:
            # Get values from HTML form
            N = float(request.form["N"])
            P = float(request.form["P"])
            K = float(request.form["K"])

            temperature = float(request.form["temperature"])
            humidity = float(request.form["humidity"])
            ph = float(request.form["ph"])
            rainfall = float(request.form["rainfall"])

            # Input validation
            if N < 0 or P < 0 or K < 0:
                raise ValueError("NPK values cannot be negative.")

            if not 0 <= humidity <= 100:
                raise ValueError("Humidity must be between 0 and 100.")

            if not 0 <= ph <= 14:
                raise ValueError("Soil pH must be between 0 and 14.")

            if rainfall < 0:
                raise ValueError("Rainfall cannot be negative.")

            # Prepare input data for ML model
            user_data = pd.DataFrame(
                [[N, P, K, temperature, humidity, ph, rainfall]],
                columns=[
                    "N",
                    "P",
                    "K",
                    "temperature",
                    "humidity",
                    "ph",
                    "rainfall"
                ]
            )

            # Predict crop
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


# Run application
if __name__ == "__main__":
    app.run(debug=True)
