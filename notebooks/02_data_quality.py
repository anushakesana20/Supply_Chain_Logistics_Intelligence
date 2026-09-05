import pandas as pd

# Load dataset
df = pd.read_csv(
    "data/DataCoSupplyChainDataset.csv",
    encoding="latin1"
)

print("========== DATA QUALITY CHECK ==========")

# Missing values
print("\nMissing values:")
print(df.isnull().sum().sort_values(ascending=False).head(10))

# Duplicate rows
print("\nDuplicate rows:")
print(df.duplicated().sum())

# Unique orders
print("\nTotal unique orders:")
print(df["Order Id"].nunique())

# Unique customers
print("\nTotal unique customers:")
print(df["Customer Id"].nunique())

# Unique products
print("\nTotal unique products:")
print(df["Product Name"].nunique())

# Order status
print("\nOrder status:")
print(df["Order Status"].value_counts())

# Shipping modes
print("\nShipping modes:")
print(df["Shipping Mode"].value_counts())

# Delivery status
print("\nDelivery status:")
print(df["Delivery Status"].value_counts())

# Late delivery risk
print("\nLate delivery risk:")
print(df["Late_delivery_risk"].value_counts())