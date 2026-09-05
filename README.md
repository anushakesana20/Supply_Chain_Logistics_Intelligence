# Supply Chain Logistics Intelligence Project

## 📌 Project Overview

This project analyzes supply chain and logistics data to identify sales trends, delivery performance, product performance, and factors associated with late deliveries.

The project uses data analysis, SQL, machine learning, demand forecasting, and Power BI to convert raw supply chain data into useful business insights.

## 🎯 Objectives

- Understand and clean supply chain data
- Perform data quality analysis
- Analyze sales and profitability
- Analyze delivery and shipping performance
- Identify products and categories with strong performance
- Forecast future demand
- Predict late-delivery risk using Machine Learning
- Build an interactive Power BI dashboard

## 🗂️ Dataset

Dataset: DataCo Smart Supply Chain Dataset

Original dataset:
- Rows: 180,519
- Columns: 53
- Unique Orders: 65,752
- Unique Customers: 20,652
- Unique Products: 118

The dataset contains information about orders, customers, products, sales, profit, shipping, delivery status, and late-delivery risk.

## 🧹 Data Cleaning

The following data-quality checks were performed:

- Checked missing values
- Checked duplicate records
- Removed the completely empty `Product Description` column
- Handled relevant missing values
- Verified the cleaned dataset
- Loaded the cleaned data into the SQL analytical layer

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Statsmodels
- SQL
- SQLite
- Power BI
- Streamlit
- Git & GitHub

## 📊 Exploratory Data Analysis

The analysis covers:

- Sales trends
- Profit analysis
- Order analysis
- Category performance
- Product performance
- Regional sales
- Shipping modes
- Delivery status
- Late-delivery risk

## 📈 Key Business Results

- Total Sales: ₹36,784,735.01
- Total Profit: ₹3,966,902.97
- Total Records: 180,519
- Unique Orders: 65,752
- Unique Customers: 20,652
- Unique Products: 118
- Late-delivery records: 98,977
- Late-delivery rate: 54.83%

First Class shipping showed the highest observed late-delivery rate in the analyzed data.

## 🔮 Demand Forecasting

A demand forecasting model was developed using monthly sales data.

### Dataset

- Monthly observations: 37
- Training observations: 30
- Testing observations: 7

### Evaluation

- MAE: 277,036.77
- RMSE: 373,534.00
- MAPE: 58.43%

A seasonal-naive forecasting approach was used, where future monthly demand is estimated using the corresponding month from the previous year.

## 🤖 Late Delivery Prediction

A Machine Learning model was developed to predict `Late_delivery_risk`.

### Features Used

- Days for shipment (scheduled)
- Shipping Mode
- Market
- Order Region
- Category Name
- Sales
- Order Item Quantity
- Product Price

### Model

Random Forest Classifier

### Dataset Split

- Training samples: 144,415
- Testing samples: 36,104

### Model Performance

- Accuracy: 68.73%

Confusion Matrix:

```text
[[13521,  2787],
 [ 8501, 11295]]