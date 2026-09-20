from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib


# Create FastAPI application
app = FastAPI(
    title="Supply Chain Logistics Intelligence API",
    description="API for late-delivery prediction and supply chain analytics",
    version="1.0"
)


# Load ML model and feature names
model = joblib.load("models/late_delivery_model.pkl")
feature_names = joblib.load("models/feature_names.pkl")


# Load cleaned dataset
data = pd.read_csv(
    "data/processed/DataCoSupplyChain_Cleaned.csv"
)


# -----------------------------
# Home endpoint
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Supply Chain Logistics Intelligence API is running"
    }


# -----------------------------
# Late Delivery Prediction
# -----------------------------

class PredictionInput(BaseModel):
    scheduled_days: int
    shipping_mode: str
    market: str
    order_region: str
    category_name: str
    sales: float
    quantity: int
    product_price: float


@app.post("/predict-delay")
def predict_delay(input_data: PredictionInput):

    input_df = pd.DataFrame([{
        "Days for shipment (scheduled)": input_data.scheduled_days,
        "Shipping Mode": input_data.shipping_mode,
        "Market": input_data.market,
        "Order Region": input_data.order_region,
        "Category Name": input_data.category_name,
        "Sales": input_data.sales,
        "Order Item Quantity": input_data.quantity,
        "Product Price": input_data.product_price
    }])

    # Convert categorical variables into dummy variables
    input_encoded = pd.get_dummies(input_df)

    # Make sure columns match the trained model
    input_encoded = input_encoded.reindex(
        columns=feature_names,
        fill_value=0
    )

    # Prediction
    prediction = model.predict(input_encoded)[0]

    probabilities = model.predict_proba(input_encoded)[0]

    on_time_probability = float(probabilities[0])
    late_probability = float(probabilities[1])

    if prediction == 1:
        result = "LATE DELIVERY"
        risk = "HIGH"
    else:
        result = "ON TIME"
        risk = "LOW"

    return {
        "prediction": result,
        "risk_level": risk,
        "on_time_probability": round(on_time_probability * 100, 2),
        "late_probability": round(late_probability * 100, 2)
    }


# -----------------------------
# Product information
# -----------------------------

@app.get("/product/{product_id}")
def product_information(product_id: int):

    product_data = data[
        data["Product Card Id"] == product_id
    ]

    if product_data.empty:
        return {
            "message": "Product not found"
        }

    return {
        "product_id": product_id,
        "product_name": product_data["Product Name"].iloc[0],
        "category": product_data["Category Name"].iloc[0],
        "total_sales": round(float(product_data["Sales"].sum()), 2),
        "total_quantity": int(
            product_data["Order Item Quantity"].sum()
        ),
        "number_of_orders": int(
            product_data["Order Id"].nunique()
        )
    }


# -----------------------------
# Region information
# -----------------------------

@app.get("/region/{region}")
def region_information(region: str):

    region_data = data[
        data["Order Region"].str.lower() == region.lower()
    ]

    if region_data.empty:
        return {
            "message": "Region not found"
        }

    late_rate = (
        region_data["Late_delivery_risk"].mean() * 100
    )

    return {
        "region": region,
        "total_sales": round(float(region_data["Sales"].sum()), 2),
        "total_units": int(
            region_data["Order Item Quantity"].sum()
        ),
        "number_of_orders": int(
            region_data["Order Id"].nunique()
        ),
        "late_delivery_rate": round(float(late_rate), 2),
        "average_delivery_days": round(
            float(
                region_data["Days for shipping (real)"].mean()
            ),
            2
        )
    }
