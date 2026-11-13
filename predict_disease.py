
import torch
import json
from PIL import Image
from torchvision import transforms
from src.mobilenet_model import PlantDiseaseMobileNet

# 1. Select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 2. Load disease classes
with open("models/disease_classes.json", "r") as file:
    class_names = json.load(file)

# 3. Load trained model
model = PlantDiseaseMobileNet(num_classes=len(class_names))

checkpoint = torch.load(
    "models/plant_disease_mobilenet.pth",
    map_location=device,
    weights_only=True
)

if "model_state_dict" in checkpoint:
    checkpoint = checkpoint["model_state_dict"]
elif "state_dict" in checkpoint:
    checkpoint = checkpoint["state_dict"]

model.load_state_dict(checkpoint)
model.to(device)
model.eval()

# 4. Image preprocessing
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 5. Take leaf image path
import random
import os

folder_path = "data/plant_disease/raw/Grape___Black_rot"

images = [
    file for file in os.listdir(folder_path)
    if file.lower().endswith((".jpg", ".jpeg", ".png"))
]

image_name = random.choice(images)
image_path = os.path.join(folder_path, image_name)

print("Selected image:", image_name)

image = Image.open(image_path).convert("RGB")
image_tensor = transform(image).unsqueeze(0).to(device)

# 6. Predict disease
with torch.no_grad():
    outputs = model(image_tensor)
    probabilities = torch.softmax(outputs, dim=1)

    confidence, predicted = torch.max(probabilities, dim=1)

predicted_class = class_names[predicted.item()]

print("\n----- AgriNova Disease Prediction -----")
print("Predicted Disease:", predicted_class)
print("Confidence:", round(confidence.item() * 100, 2), "%")
# Convert class name into readable format
readable_name = predicted_class.replace("___", " - ").replace("_", " ")

# Basic disease information
disease_info = {
    "Grape___Black_rot": {
        "symptoms": "Dark brown or black spots on leaves and berries.",
        "care": "Remove infected plant parts, maintain proper airflow, "
                "avoid overhead watering and seek local agricultural guidance."
    }
}

print("\n----- Disease Information -----")
print("Disease:", readable_name)

if predicted_class in disease_info:
    info = disease_info[predicted_class]
    print("Symptoms:", info["symptoms"])
    print("Care:", info["care"])