import pandas as pd

# Load dataset
df = pd.read_csv("data/crop_data.csv")

# Display first 5 rows
print("First 5 Rows:")
print(df.head())

# Dataset dimensions
print("\nDataset Shape:")
print(df.shape)

# Dataset information
print("\nDataset Information:")
print(df.info())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDuplicate Rows:", df.duplicated().sum())