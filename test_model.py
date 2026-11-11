
import torch
from src.disease_model import PlantDiseaseCNN

num_classes = 38

model = PlantDiseaseCNN(num_classes)

dummy_input = torch.randn(1, 3, 128, 128)

output = model(dummy_input)

print("Output shape:", output.shape)
print("CNN model created successfully!")
