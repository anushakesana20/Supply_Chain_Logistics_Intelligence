import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


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
# 4. Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 5. Load trained model
# ==========================================

model = joblib.load(
    "models/late_delivery_model.pkl"
)

print("Model loaded successfully!")


# ==========================================
# 6. Make predictions
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 7. Accuracy
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n========== MODEL EVALUATION ==========")

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
        y_pred
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
    display_labels=[
        "On-Time",
        "Late"
    ]
)

display.plot()

plt.title(
    "Confusion Matrix - Late Delivery Prediction"
)

plt.tight_layout()

plt.show()


print("\n========== DONE ==========")