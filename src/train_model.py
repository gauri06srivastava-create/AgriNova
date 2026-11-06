import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned_crop_data.csv")

# Display columns
print("Columns:")
print(df.columns)

# Display crop categories
print("\nCrop Categories:")
print(df["label"].unique())

# Count each crop
print("\nCrop Distribution:")
print(df["label"].value_counts())