import pandas as pd

# ==========================================
# 1. Load cleaned dataset
# ==========================================

df = pd.read_csv(
    "data/processed/DataCoSupplyChain_Cleaned.csv",
    encoding="utf-8",
    low_memory=False
)

print("Original dataset shape:", df.shape)


# ==========================================
# 2. Select ML features
# ==========================================

features = [
    "Days for shipment (scheduled)",
    "Shipping Mode",
    "Market",
    "Order Region",
    "Category Name",
    "Sales",
    "Order Item Quantity",
    "Product Price"
]

target = "Late_delivery_risk"


# ==========================================
# 3. Create X and y
# ==========================================

X = df[features].copy()
y = df[target].copy()


# ==========================================
# 4. Display information
# ==========================================

print("\n========== FEATURES ==========")
print(X.columns.tolist())

print("\n========== TARGET ==========")
print(target)

print("\nFeature shape:", X.shape)
print("Target shape:", y.shape)

print("\n========== TARGET DISTRIBUTION ==========")
print(y.value_counts())

print("\n========== MISSING VALUES ==========")
print(X.isnull().sum())

print("\n========== DATA TYPES ==========")
print(X.dtypes)


# ==========================================
# 5. Convert categorical columns
# ==========================================

categorical_columns = [
    "Shipping Mode",
    "Market",
    "Order Region",
    "Category Name"
]

X = pd.get_dummies(
    X,
    columns=categorical_columns,
    drop_first=True
)


# ==========================================
# 6. Handle missing values
# ==========================================

X = X.fillna(0)


# ==========================================
# 7. Final ML data
# ==========================================

print("\n========== FINAL ML DATA ==========")
print("X shape:", X.shape)
print("y shape:", y.shape)

print("\nMissing values after preprocessing:")
print(X.isnull().sum().sum())

print("\nML preparation completed successfully!")