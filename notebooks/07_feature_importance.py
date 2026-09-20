import pandas as pd
import matplotlib.pyplot as plt
import os
import joblib

from sklearn.ensemble import RandomForestClassifier


# ==========================================
# 1. Load cleaned dataset
# ==========================================

df = pd.read_csv(
    "data/processed/DataCoSupplyChain_Cleaned.csv",
    encoding="utf-8",
    low_memory=False
)

print("Dataset shape:", df.shape)


# ==========================================
# 2. Select features and target
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


X = df[features].copy()
y = df[target].copy()


# ==========================================
# 3. Convert categorical columns
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

X = X.fillna(0)


# ==========================================
# 4. Train Random Forest
# ==========================================

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

print("Model training completed!")


# ==========================================
# 5. Feature Importance
# ==========================================

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)
importance.to_csv(
    "data/processed/feature_importance.csv",
    index=False
)

print("Feature importance CSV saved successfully!")
print("\n========== TOP 15 IMPORTANT FEATURES ==========")

print(importance.head(15).to_string(index=False))


# ==========================================
# 6. Plot Top 15 Features
# ==========================================

top_features = importance.head(15).sort_values(
    by="Importance"
)

plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 15 Features Affecting Late Delivery Risk")

plt.tight_layout()
plt.show()


# ==========================================
# 7. Create models folder
# ==========================================

os.makedirs("models", exist_ok=True)


# ==========================================
# 8. Save trained model
# ==========================================

joblib.dump(
    model,
    "models/late_delivery_model.pkl"
)

print("\nModel saved successfully!")


# ==========================================
# 9. Save feature names
# ==========================================

joblib.dump(
    list(X.columns),
    "models/feature_names.pkl"
)

print("Feature names saved successfully!")

print("\n========== DONE ==========")