
import torch
import torch.nn as nn
import torch.optim as optim
import json
from tqdm import tqdm

from src.disease_model import PlantDiseaseCNN
from src.disease_data import dataset, train_loader, val_loader

# Select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Training device:", device)

# Create model
num_classes = len(dataset.classes)
model = PlantDiseaseCNN(num_classes).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train for 3 epochs initially
epochs = 3

for epoch in range(epochs):

    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    print(f"\nEpoch {epoch+1}/{epochs}")

    # Training
    progress_bar = tqdm(train_loader, desc="Training")

    for images, labels in progress_bar:

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

        progress_bar.set_postfix(loss=f"{loss.item():.4f}")

    train_accuracy = 100 * correct / total

    # Validation
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

    print(f"Training Loss: {running_loss/len(train_loader):.4f}")
    print(f"Training Accuracy: {train_accuracy:.2f}%")
    print(f"Validation Accuracy: {val_accuracy:.2f}%")

# Save trained model
torch.save(
    model.state_dict(),
    "models/plant_disease_model.pth"
)

# Save disease class names
with open("models/disease_classes.json", "w") as file:
    json.dump(dataset.classes, file)

print("\nModel training completed!")
print("Model and class names saved successfully!")
