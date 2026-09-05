import pandas as pd

# Load dataset
df = pd.read_csv(
    "data/DataCoSupplyChainDataset.csv",
    encoding="latin1"
)

# 1. Dataset size
print("DATASET SHAPE:")
print(df.shape)

# 2. Column names
print("\nCOLUMN NAMES:")
print(df.columns.tolist())

# 3. First 5 rows
print("\nFIRST 5 ROWS:")
print(df.head())

# 4. Data types
print("\nDATA TYPES:")
print(df.dtypes)

# 5. Missing values
print("\nMISSING VALUES:")
print(df.isnull().sum().sort_values(ascending=False).head(10))

# 6. Duplicate rows
print("\nDUPLICATE ROWS:")
print(df.duplicated().sum())