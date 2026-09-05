import pandas as pd
import joblib


# ==========================================
# 1. Load trained model
# ==========================================

model = joblib.load(
    "models/late_delivery_model.pkl"
)

feature_names = joblib.load(
    "models/feature_names.pkl"
)

print("Model loaded successfully!")


# ==========================================
# 2. New order details
# ==========================================

new_order = pd.DataFrame([{
    "Days for shipment (scheduled)": 4,
    "Shipping Mode": "Standard Class",
    "Market": "Europe",
    "Order Region": "Western Europe",
    "Category Name": "Fishing",
    "Sales": 500,
    "Order Item Quantity": 2,
    "Product Price": 250
}])


# ==========================================
# 3. Convert categorical columns
# ==========================================

categorical_columns = [
    "Shipping Mode",
    "Market",
    "Order Region",
    "Category Name"
]

new_order = pd.get_dummies(
    new_order,
    columns=categorical_columns,
    drop_first=True
)


# ==========================================
# 4. Match training features
# ==========================================

new_order = new_order.reindex(
    columns=feature_names,
    fill_value=0
)


# ==========================================
# 5. Make prediction
# ==========================================

prediction = model.predict(new_order)[0]

probability = model.predict_proba(new_order)[0]


# ==========================================
# 6. Display result
# ==========================================

print("\n========== DELIVERY PREDICTION ==========")

if prediction == 1:
    print("Prediction: LATE DELIVERY")
    print("Risk Level: HIGH")
else:
    print("Prediction: ON-TIME DELIVERY")
    print("Risk Level: LOW")


print("\nProbability:")
print("On-time:", round(probability[0] * 100, 2), "%")
print("Late:", round(probability[1] * 100, 2), "%")

print("\n========== DONE ==========")
