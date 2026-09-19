# Supply Chain Logistics Intelligence Project

## 📌 Project Overview

This project analyzes supply chain and logistics data to identify sales trends, delivery performance, product performance, demand patterns, and factors associated with late deliveries.

The project uses data analysis, SQL, machine learning, demand forecasting, and Power BI to convert raw supply chain data into useful business insights.

The project follows the workflow:

Raw Data → Data Cleaning → SQL Analysis → EDA → KPI Analysis → Demand Forecasting → ML Prediction → Power BI Dashboard

---

## 🎯 Objectives

- Understand and clean supply chain data
- Perform data quality analysis
- Analyze sales and profitability
- Analyze delivery and shipping performance
- Identify products and categories with strong performance
- Analyze demand trends
- Forecast future demand
- Predict late-delivery risk using Machine Learning
- Build an interactive Power BI dashboard
- Document business insights and limitations

---

## 🗂️ Dataset

**Dataset:** DataCo Smart Supply Chain Dataset

### Original Dataset

- Rows: 180,519
- Columns: 53
- Unique Orders: 65,752
- Unique Customers: 20,652
- Unique Products: 118

The dataset contains information about orders, customers, products, sales, profit, shipping, delivery status, and late-delivery risk.

### Data Grain

The dataset is at the **order-item level**. Therefore, a single order can contain multiple rows.

Because of this, order-level and customer-level metrics are calculated using distinct Order IDs and Customer IDs where required instead of simply counting rows.

---

## 🧹 Data Cleaning

The following data-quality checks were performed:

- Checked missing values
- Checked duplicate records
- Checked unique orders, customers, and products
- Checked categorical distributions
- Removed the completely empty `Product Description` column
- Handled relevant missing values
- Converted date columns into datetime format
- Verified the cleaned dataset
- Saved the cleaned dataset separately from the raw dataset
- Loaded the cleaned data into the SQL analytical layer

No duplicate rows were identified in the original dataset.

---

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
- Git
- GitHub

---

## 📊 Exploratory Data Analysis

The analysis covers:

- Sales trends
- Profit analysis
- Order analysis
- Category performance
- Product performance
- Regional sales
- Customer segments
- Shipping modes
- Delivery status
- Late-delivery risk
- Delivery performance
- Demand trends

---

## 🧮 SQL Analysis

SQL was used to perform operational and management-level analysis.

The analysis includes:

- Total records
- Unique orders
- Unique customers
- Unique products
- Order status distribution
- Shipping mode distribution
- Delivery status distribution
- Total sales
- Total profit
- Sales by category
- Profit by category
- Sales by region
- Late-delivery rate by shipping mode
- Late-delivery rate by region
- Late-delivery rate by market
- Units sold
- Average order value
- Average delivery duration
- Customer segment analysis
- Product and regional rankings
- Monthly sales trends
- Month-over-month sales analysis
- Cumulative sales
- Demand variability
- Fast and slow product movers

Advanced SQL concepts such as `CASE`, `CTE`, `LAG`, `RANK`, and conditional aggregation were also used where applicable.

---

## 📈 Key Business Results

- **Total Sales:** ₹36,784,735.01
- **Total Profit:** ₹3,966,902.97
- **Total Records:** 180,519
- **Unique Orders:** 65,752
- **Unique Customers:** 20,652
- **Unique Products:** 118
- **Late-delivery records:** 98,977
- **Late-delivery rate:** 54.83%

Among the analyzed shipping modes, **First Class had the highest observed late-delivery rate**.

---

## 🔮 Demand Forecasting

A demand forecasting model was developed using monthly sales data.

### Dataset

- Monthly observations: 37
- Training observations: 30
- Testing observations: 7
- Forecast horizon: 6 future months

### Models Compared

Two forecasting approaches were evaluated:

1. Naive Baseline
2. Seasonal Naive

### Naive Baseline Performance

- **MAE:** 131,973.37
- **RMSE:** 191,232.60
- **MAPE:** 23.45%

### Seasonal Naive Performance

- **MAE:** 277,036.77
- **RMSE:** 373,534.00
- **MAPE:** 58.43%

The **Naive Baseline was selected based on lower MAE, RMSE, and MAPE**.

The selected model uses the latest observed monthly demand as the baseline for future demand planning.

### Business Use

The forecast can support:

- Demand planning
- Inventory planning
- Logistics capacity planning
- Replenishment planning

The dataset does not contain actual inventory stock levels. Therefore, the forecast is used as a **demand-planning indicator**, not as an actual stock-out prediction.

---

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

**Random Forest Classifier**

### Dataset Split

- Training samples: 144,415
- Testing samples: 36,104

### Model Performance

- Random Forest Accuracy: **68.73%**
- Majority Class Baseline Accuracy: **54.83%**

The Random Forest model therefore provides additional predictive information compared with the simple majority-class baseline.

### Confusion Matrix

```text
[[13521, 2787],
 [ 8501,11295]]