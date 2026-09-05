import pandas as pd

# Load cleaned dataset
df = pd.read_csv(
    "data/processed/DataCoSupplyChain_Cleaned.csv",
    encoding="utf-8"
)

print("========== CLEANED DATASET ==========")

# Dataset size
print("\nDataset Shape:")
print(df.shape)

# Check Product Description
print("\nProduct Description present?")
print("Product Description" in df.columns)

# Duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Missing values
print("\nMissing Values:")
print(df.isnull().sum().sort_values(ascending=False).head(10))

# First 5 rows
print("\nFirst 5 Rows:")
print(df.head())