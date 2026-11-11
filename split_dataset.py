
from torchvision import datasets, transforms
from torch.utils.data import random_split

dataset_path = "data/plant_disease/raw"

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor()
])

dataset = datasets.ImageFolder(
    root=dataset_path,
    transform=transform
)

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train_dataset, val_dataset = random_split(
    dataset,
    [train_size, val_size]
)

print("Total images:", len(dataset))
print("Training images:", len(train_dataset))
print("Validation images:", len(val_dataset))
print("Disease classes:", len(dataset.classes))
