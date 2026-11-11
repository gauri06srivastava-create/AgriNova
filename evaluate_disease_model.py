
import torch
import matplotlib.pyplot as plt
import os

from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

from src.disease_model import PlantDiseaseCNN
from src.disease_data import dataset, val_loader

# 1. Select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 2. Load trained model
num_classes = len(dataset.classes)

model = PlantDiseaseCNN(num_classes).to(device)

model.load_state_dict(
    torch.load(
        "models/plant_disease_model.pth",
        map_location=device
    )
)

model.eval()

# 3. Store predictions and actual labels
all_predictions = []
all_labels = []

with torch.no_grad():

    for images, labels in val_loader:

        images = images.to(device)

        outputs = model(images)

        _, predicted = torch.max(outputs, 1)

        all_predictions.extend(predicted.cpu().numpy())
        all_labels.extend(labels.numpy())

# 4. Generate classification report
report = classification_report(
    all_labels,
    all_predictions,
    labels=list(range(num_classes)),
    target_names=dataset.classes,
    zero_division=0
)

print("\nCLASSIFICATION REPORT")
print(report)

# 5. Generate confusion matrix
cm = confusion_matrix(
    all_labels,
    all_predictions,
    labels=list(range(num_classes))
)

os.makedirs("reports", exist_ok=True)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=dataset.classes
)

fig, ax = plt.subplots(figsize=(20, 18))

display.plot(
    ax=ax,
    xticks_rotation=90,
    cmap="Blues",
    colorbar=False
)

plt.title("AgriNova - Plant Disease Confusion Matrix")
plt.tight_layout()

plt.savefig("reports/confusion_matrix.png")
plt.close()

# 6. Save classification report
with open("reports/classification_report.txt", "w") as file:
    file.write(report)

print("\nEvaluation completed!")
print("Reports saved in reports folder.")
