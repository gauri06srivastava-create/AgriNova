
from torchvision import datasets, transforms

dataset_path = "data/plant_disease/raw"

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor()
])

dataset = datasets.ImageFolder(
    root=dataset_path,
    transform=transform
)

print("Total images:", len(dataset))
print("Total classes:", len(dataset.classes))

print("\nDisease categories:")

for class_name in dataset.classes:
    print(class_name)
