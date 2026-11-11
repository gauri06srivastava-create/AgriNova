
from pathlib import Path

dataset_path = Path("data/plant_disease/raw")

classes = [
    folder for folder in dataset_path.iterdir()
    if folder.is_dir()
]

print("Total disease classes:", len(classes))
print("-" * 40)

total_images = 0

for folder in sorted(classes):
    images = [
        file for file in folder.iterdir()
        if file.suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]

    count = len(images)
    total_images += count

    print(folder.name, ":", count, "images")

print("-" * 40)
print("Total images:", total_images)
