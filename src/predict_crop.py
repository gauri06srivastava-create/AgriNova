import pickle
import pandas as pd
# Load saved model
with open("models/crop_model.pkl", "rb") as file:
    model = pickle.load(file)

print("AgriNova Crop Prediction System")

# Take user input
N = float(input("Nitrogen: "))
P = float(input("Phosphorus: "))
K = float(input("Potassium: "))
temperature = float(input("Temperature: "))
humidity = float(input("Humidity: "))
ph = float(input("Soil pH: "))
rainfall = float(input("Rainfall: "))

# Predict crop
user_data = pd.DataFrame([[
    N, P, K, temperature, humidity, ph, rainfall
]], columns=[
    "N", "P", "K", "temperature",
    "humidity", "ph", "rainfall"
])

prediction = model.predict(user_data)

print("\nRecommended Crop:", prediction[0])