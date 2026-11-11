
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
from collections import defaultdict

DATASET_PATH = "data/plant_disease/raw"
IMAGES_PER_CLASS = 100

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

dataset = datasets.ImageFolder(
    root=DATASET_PATH,
    transform=transform
)

# Group images class-wise
class_indices = defaultdict(list)

for index, label in enumerate(dataset.targets):
    class_indices[label].append(index)

# Select 100 images from every class
generator = torch.Generator().manual_seed(42)

train_indices = []
val_indices = []

for class_id in range(len(dataset.classes)):
    indices = class_indices[class_id]

    shuffled = torch.randperm(
        len(indices),
        generator=generator
    ).tolist()

    selected = [indices[i] for i in shuffled[:IMAGES_PER_CLASS]]

    split = int(0.8 * len(selected))

    train_indices.extend(selected[:split])
    val_indices.extend(selected[split:])

train_dataset = Subset(dataset, train_indices)
val_dataset = Subset(dataset, val_indices)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0
)

print("Total sampled images:", len(train_indices) + len(val_indices))
print("Training images:", len(train_indices))
print("Validation images:", len(val_indices))
print("Training batches:", len(train_loader))
print("Validation batches:", len(val_loader))
print("Disease classes:", len(dataset.classes))
