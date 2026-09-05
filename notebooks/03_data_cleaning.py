import pandas as pd
import os

# Load raw dataset
df = pd.read_csv(
    "data/DataCoSupplyChainDataset.csv",
    encoding="latin1"
)

print("Original shape:", df.shape)

# --------------------------------
# 1. Remove completely empty columns
# --------------------------------

empty_columns = df.columns[df.isnull().all()].tolist()

print("\nCompletely empty columns:")
print(empty_columns)

df = df.dropna(axis=1, how="all")

# --------------------------------
# 2. Convert date columns
# --------------------------------

df["order date (DateOrders)"] = pd.to_datetime(
    df["order date (DateOrders)"],
    errors="coerce"
)

df["shipping date (DateOrders)"] = pd.to_datetime(
    df["shipping date (DateOrders)"],
    errors="coerce"
)

# --------------------------------
# 3. Fill small missing values
# --------------------------------

if "Customer Lname" in df.columns:
    df["Customer Lname"] = df["Customer Lname"].fillna("Unknown")

if "Customer Zipcode" in df.columns:
    df["Customer Zipcode"] = df["Customer Zipcode"].fillna("Unknown")

# --------------------------------
# 4. Check missing values again
# --------------------------------

print("\nMissing values after cleaning:")
print(df.isnull().sum().sort_values(ascending=False).head(10))

# --------------------------------
# 5. Save cleaned dataset
# --------------------------------

# --------------------------------
# 5. Save cleaned dataset
# --------------------------------

output_path = "data/processed/DataCoSupplyChain_Cleaned.csv"

df.to_csv(output_path, index=False, encoding="utf-8")

print("\nCleaned shape:", df.shape)
print("\nCleaned dataset saved to:")
print(output_path)