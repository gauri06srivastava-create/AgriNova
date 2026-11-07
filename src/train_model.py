import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("data/cleaned_crop_data.csv")

# Separate features and target
X = df.drop("label", axis=1)
y = df["label"]

# Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Display results
print("Total Dataset:", df.shape)

print("Training Features:", X_train.shape)
print("Testing Features:", X_test.shape)

print("Training Labels:", y_train.shape)
print("Testing Labels:", y_test.shape)
# Create Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

print("\nModel Training Completed!")
# Predict crops
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy * 100, "%")
# Classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
# Take user input
print("\nEnter Soil and Weather Details:")

N = float(input("Nitrogen: "))
P = float(input("Phosphorus: "))
K = float(input("Potassium: "))
temperature = float(input("Temperature: "))
humidity = float(input("Humidity: "))
ph = float(input("Soil pH: "))
rainfall = float(input("Rainfall: "))

# Predict crop
user_data = [[N, P, K, temperature, humidity, ph, rainfall]]

prediction = model.predict(user_data)

print("\nRecommended Crop:", prediction[0])
# Save trained model
with open("models/crop_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel Saved Successfully!")