
import torch
import json
from PIL import Image
from torchvision import transforms
from src.mobilenet_model import PlantDiseaseMobileNet


# Select device
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# Load disease class names
with open("models/disease_classes.json", "r") as file:
    class_names = json.load(file)


# Load trained MobileNetV2 model
model = PlantDiseaseMobileNet(
    num_classes=len(class_names)
)

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


# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# Prediction function
def predict_disease(image_path):

    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)

        confidence, predicted = torch.max(
            probabilities, dim=1
        )

    predicted_class = class_names[predicted.item()]

    return predicted_class, confidence.item() * 100
