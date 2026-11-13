
import torch
from src.mobilenet_model import PlantDiseaseMobileNet

# Number of disease categories
num_classes = 38

# Create model
model = PlantDiseaseMobileNet(num_classes)

# Create a dummy leaf image
dummy_input = torch.randn(1, 3, 128, 128)

# Make prediction
output = model(dummy_input)

print("Output shape:", output.shape)
print("MobileNetV2 loaded successfully!")
print("Total parameters:", sum(p.numel() for p in model.parameters()))
print(
    "Trainable parameters:",
    sum(p.numel() for p in model.parameters() if p.requires_grad)
)
