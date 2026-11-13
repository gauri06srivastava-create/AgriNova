
import torch
import torch.nn as nn
import torch.optim as optim
import json
import os

from tqdm import tqdm
from src.mobilenet_model import PlantDiseaseMobileNet
from src.disease_data import dataset, train_loader, val_loader

# 1. Select device
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Training device:", device)

# 2. Create model
num_classes = len(dataset.classes)

model = PlantDiseaseMobileNet(num_classes).to(device)

# 3. Loss function
criterion = nn.CrossEntropyLoss()

# 4. Optimize only trainable parameters
optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=0.001
)

# 5. Training settings
epochs = 5
best_accuracy = 0.0

os.makedirs("models", exist_ok=True)

for epoch in range(epochs):

    model.train()

    # Keep pretrained feature extractor in evaluation mode
    model.model.features.eval()

    running_loss = 0.0
    correct = 0
    total = 0

    print(f"\nEpoch {epoch + 1}/{epochs}")

    for images, labels in tqdm(train_loader, desc="Training"):

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        _, predicted = torch.max(outputs, 1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    train_accuracy = 100 * correct / total

    # 6. Validation
    model.eval()

    val_correct = 0
    val_total = 0

    with torch.no_grad():

        for images, labels in tqdm(val_loader, desc="Validation"):

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()

    val_accuracy = 100 * val_correct / val_total

    print(f"Training Loss: {running_loss / len(train_loader):.4f}")
    print(f"Training Accuracy: {train_accuracy:.2f}%")
    print(f"Validation Accuracy: {val_accuracy:.2f}%")

    # 7. Save best model
    if val_accuracy > best_accuracy:

        best_accuracy = val_accuracy

        torch.save(
            model.state_dict(),
            "models/plant_disease_mobilenet.pth"
        )

        print("Best model saved!")

# Save class names
with open("models/disease_classes.json", "w") as file:
    json.dump(dataset.classes, file)

print("\nMobileNetV2 training completed!")
print(f"Best validation accuracy: {best_accuracy:.2f}%")
