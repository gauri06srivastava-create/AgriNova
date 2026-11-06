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
# Remove duplicate rows
df = df.drop_duplicates()

# Handle missing values
df = df.dropna()

# Display cleaned dataset
print("\nAfter Cleaning:")
print("Shape:", df.shape)
print("Missing Values:", df.isnull().sum().sum())
print("Duplicates:", df.duplicated().sum())

# Save cleaned dataset
df.to_csv("data/cleaned_crop_data.csv", index=False)

print("\nCleaned dataset saved successfully!")