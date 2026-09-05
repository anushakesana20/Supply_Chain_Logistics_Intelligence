import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


# ==========================================
# 1. Load dataset
# ==========================================

df = pd.read_csv(
    "data/processed/DataCoSupplyChain_Cleaned.csv",
    encoding="utf-8",
    low_memory=False
)

print("Dataset shape:", df.shape)


# ==========================================
# 2. Features and target
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
# 3. Encode categorical columns
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
# 4. Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n========== DATA SPLIT ==========")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 5. Train model ONLY on training data
# ==========================================

print("\nTraining final model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 6. Prediction on unseen test data
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 7. Accuracy
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n========== FINAL MODEL RESULTS ==========")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


# ==========================================
# 8. Classification Report
# ==========================================

print("\n========== CLASSIFICATION REPORT ==========")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["On-Time", "Late"]
    )
)


# ==========================================
# 9. Confusion Matrix
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\n========== CONFUSION MATRIX ==========")
print(cm)


# ==========================================
# 10. Display Confusion Matrix
# ==========================================

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["On-Time", "Late"]
)

display.plot()

plt.title(
    "Final Model - Confusion Matrix"
)

plt.tight_layout()
plt.show()


# ==========================================
# 11. Feature Importance
# ==========================================

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n========== TOP 15 FEATURES ==========")

print(
    importance.head(15).to_string(index=False)
)


# ==========================================
# 12. Save final model
# ==========================================

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/late_delivery_model.pkl"
)

joblib.dump(
    list(X.columns),
    "models/feature_names.pkl"
)

print("\nFinal model saved successfully!")

print("Feature names saved successfully!")

print("\n========== FINAL MODEL COMPLETE ==========")