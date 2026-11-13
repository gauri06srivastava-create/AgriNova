
import torch
import json
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from src.disease_data import val_loader, dataset
from src.mobilenet_model import PlantDiseaseMobileNet

# Select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load class names
with open("models/disease_classes.json", "r") as file:
    class_names = json.load(file)

# Load trained model
model = PlantDiseaseMobileNet(num_classes=len(class_names))

checkpoint = torch.load(
    "models/plant_disease_mobilenet.pth",
    map_location=device
)

# Support either a direct state dictionary or a checkpoint dictionary
if "model_state_dict" in checkpoint:
    model.load_state_dict(checkpoint["model_state_dict"])
else:
    model.load_state_dict(checkpoint)

model.to(device)
model.eval()

# Make predictions
all_predictions = []
all_labels = []

with torch.no_grad():
    for images, labels in val_loader:
        images = images.to(device)

        outputs = model(images)
        predictions = torch.argmax(outputs, dim=1)

        all_predictions.extend(predictions.cpu().numpy())
        all_labels.extend(labels.numpy())

# Calculate evaluation metrics
print("\nClassification Report:\n")

print(classification_report(
    all_labels,
    all_predictions,
    labels=list(range(len(class_names))),
    target_names=class_names,
    zero_division=0
))

print("\nConfusion Matrix:\n")
print(confusion_matrix(all_labels, all_predictions))

print("\nMobileNetV2 evaluation completed!")
