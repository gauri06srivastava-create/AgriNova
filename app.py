from flask import Flask, render_template, request
import pickle
import pandas as pd

# Create Flask app
app = Flask(__name__)

# Load trained ML model
with open("models/crop_model.pkl", "rb") as file:
    model = pickle.load(file)


# Home route
@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None

    if request.method == "POST":

        # Get input values
        N = float(request.form["N"])
        P = float(request.form["P"])
        K = float(request.form["K"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])

        # Prepare input data
        user_data = pd.DataFrame([[
            N, P, K, temperature, humidity, ph, rainfall
        ]], columns=[
            "N", "P", "K", "temperature",
            "humidity", "ph", "rainfall"
        ])

        # Predict crop
        prediction = model.predict(user_data)[0]

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)