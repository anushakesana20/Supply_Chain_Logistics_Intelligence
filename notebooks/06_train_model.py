import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


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
# 2. Select features
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
# 4. Convert categorical columns
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
# 5. Handle missing values
# ==========================================

X = X.fillna(0)


# ==========================================
# 6. Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n========== TRAIN TEST SPLIT ==========")

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

print("Training features:", X_train.shape[1])
print("Testing features:", X_test.shape[1])


# ==========================================
# 7. Create Random Forest model
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# ==========================================
# 8. Train model
# ==========================================

print("\nTraining model...")

model.fit(X_train, y_train)

print("Model training completed!")


# ==========================================
# 9. Make predictions
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 10. Model evaluation
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\n========== MODEL RESULTS ==========")

print("Accuracy:", accuracy)
# ============================================================
# SIMPLE BASELINE COMPARISON
# ============================================================

majority_class = y_test.mode()[0]

baseline_predictions = np.full(
    len(y_test),
    majority_class
)

baseline_accuracy = (
    baseline_predictions == y_test
).mean()

print("\n========== BASELINE COMPARISON ==========")

print(
    f"Majority Class Baseline Accuracy: "
    f"{baseline_accuracy:.4f}"
)

print(
    f"Random Forest Accuracy: "
    f"{accuracy:.4f}"
)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
