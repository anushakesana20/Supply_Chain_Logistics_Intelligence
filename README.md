# Supply Chain & Logistics Intelligence System

## 📌 Project Overview

The **Supply Chain & Logistics Intelligence System** is an end-to-end data analytics and machine learning project developed using the **DataCo Smart Supply Chain Dataset**.

The project analyzes sales, profitability, products, customers, regions, shipping modes, delivery performance, demand patterns, and late-delivery risk.

It combines:

* Data Cleaning
* Exploratory Data Analysis
* SQL Analytics
* KPI Analysis
* Statistical Analysis
* Demand Forecasting
* Machine Learning
* Feature Importance
* Regional Logistics Risk Analysis
* Power BI Dashboard
* Streamlit Dashboard
* FastAPI Prediction API
* GenAI-based Supply Chain Assistant

The objective is to convert raw supply-chain data into meaningful business and operational insights that can support **sales analysis, logistics monitoring, demand planning, inventory planning, and delivery-risk management**.

### Project Workflow

```text
Raw Data
   ↓
Data Understanding
   ↓
Data Quality Analysis
   ↓
Data Cleaning
   ↓
SQLite Database
   ↓
SQL Analytics
   ↓
Exploratory Data Analysis
   ↓
KPI Engineering
   ↓
Statistical Analysis
   ↓
Supplier / Inventory / Logistics Analysis
   ↓
Demand Forecasting
   ↓
Late Delivery ML Prediction
   ↓
Feature Importance
   ↓
Regional Risk Analysis
   ↓
Power BI Dashboard
   ↓
Streamlit Dashboard
   ↓
FastAPI
   ↓
GenAI Supply Chain Assistant
```

---

# 🎯 Project Objectives

The major objectives of this project are:

* Understand the structure and business meaning of supply-chain data
* Perform comprehensive data-quality analysis
* Clean and validate the dataset
* Store cleaned data in an SQL analytical layer
* Perform SQL-based business and operational analysis
* Analyze sales and profitability
* Analyze products and categories
* Analyze customers and customer segments
* Analyze regional performance
* Analyze shipping modes and delivery performance
* Calculate important supply-chain KPIs
* Perform exploratory data analysis
* Perform statistical analysis and hypothesis testing
* Identify fast-moving and slow-moving products
* Analyze demand variability
* Forecast future demand
* Predict late-delivery risk using Machine Learning
* Identify important factors affecting late deliveries
* Analyze regional logistics risk
* Build interactive Power BI dashboards
* Build a Streamlit analytical dashboard
* Provide prediction functionality through FastAPI
* Provide validated supply-chain answers through a GenAI assistant
* Document assumptions, limitations, and business interpretation

---

# 📊 Dataset

## DataCo Smart Supply Chain Dataset

The project uses the **DataCo Smart Supply Chain Dataset**.

### Original Dataset

| Metric           |   Value |
| ---------------- | ------: |
| Rows             | 180,519 |
| Columns          |      53 |
| Unique Orders    |  65,752 |
| Unique Customers |  20,652 |
| Unique Products  |     118 |

The dataset contains information related to:

* Orders
* Order items
* Customers
* Products
* Categories
* Markets
* Regions
* Sales
* Profit
* Quantity
* Shipping modes
* Shipping schedules
* Delivery performance
* Late-delivery risk

---

# 🔎 Data Grain

The dataset is at the **order-item level**.

This means that one order can contain multiple rows.

Therefore:

* Rows must not be directly interpreted as orders.
* Order-level metrics use distinct `Order Id`.
* Customer-level metrics use distinct customer identifiers where required.
* Product-level analysis uses product identifiers and product names appropriately.

This prevents incorrect calculations caused by repeated Order IDs.

---

# 🧹 Data Cleaning & Data Quality

The following data-quality checks were performed:

* Missing-value analysis
* Duplicate-record analysis
* Unique order analysis
* Unique customer analysis
* Unique product analysis
* Categorical-value analysis
* Date-column validation
* Suspicious-value checks
* Data-type validation
* Cleaned-data verification

### Important Cleaning Results

* Original dataset: **180,519 rows × 53 columns**
* Cleaned dataset: **180,519 rows × 52 columns**
* The completely empty `Product Description` column was removed.
* No duplicate rows were identified.
* Relevant missing values were examined and handled according to their analytical use.
* Date fields were converted into appropriate datetime formats.
* The cleaned dataset was saved separately from the raw dataset.

The cleaned data was then loaded into the SQLite analytical database.

---

# 🗄️ SQL Analytical Layer

The project uses **SQLite** as the SQL analytical layer.

The pipeline is:

```text
Cleaned CSV
     ↓
load_data.py
     ↓
supply_chain.db
     ↓
SQL Queries
     ↓
Business & Operational Insights
```

## SQL Analysis Includes

### Basic Analysis

* Total records
* Unique orders
* Unique customers
* Unique products
* Total sales
* Total profit
* Units sold
* Order status distribution
* Shipping mode distribution
* Delivery status distribution

### Sales Analysis

* Sales by category
* Profit by category
* Sales by region
* Sales by market
* Sales by customer segment
* Product rankings
* Regional rankings
* Monthly sales
* Month-over-month sales growth
* Cumulative sales

### Logistics Analysis

* Average delivery duration
* Delivery status
* Late-delivery rate
* Late-delivery rate by shipping mode
* Late-delivery rate by region
* Late-delivery rate by market
* Shipping-mode performance

### Product & Demand Analysis

* Product rankings
* Fast-moving products
* Slow-moving products
* Demand variability
* Product performance within categories and regions

### Advanced SQL

The project uses advanced SQL concepts where applicable:

* `CASE`
* `CTE`
* `JOIN`
* `ROW_NUMBER()`
* `RANK()`
* `DENSE_RANK()`
* `LAG()`
* Conditional aggregation
* Monthly analysis
* Regional rankings
* Cumulative calculations

---

# 📈 Exploratory Data Analysis

Exploratory analysis was performed to understand the major patterns in the supply-chain data.

The analysis covers:

* Sales trends
* Profit trends
* Order trends
* Product performance
* Category performance
* Regional sales
* Market performance
* Customer segments
* Shipping modes
* Delivery status
* Late-delivery risk
* Delivery duration
* Quantity patterns
* Demand trends
* Outlier analysis
* Relationships between numerical variables

---

# 📌 Key Business KPIs

The project calculates important supply-chain KPIs including:

* Total Revenue / Sales
* Total Profit
* Total Orders
* Total Units Sold
* Average Order Value
* Average Delivery Duration
* On-Time Delivery Rate
* Late Delivery Rate
* Sales Growth
* Category Contribution
* Regional Performance
* Shipping Mode Performance
* Product Performance

---

# 📊 Key Business Results

Based on the cleaned DataCo dataset:

| KPI                   |         Result |
| --------------------- | -------------: |
| Total Sales           | ₹36,784,735.01 |
| Total Profit          |  ₹3,966,902.97 |
| Total Records         |        180,519 |
| Unique Orders         |         65,752 |
| Unique Customers      |         20,652 |
| Unique Products       |            118 |
| Late-Delivery Records |         98,977 |
| Late-Delivery Rate    |         54.83% |
| On-Time Rate          |         45.17% |

Among the analyzed shipping modes, **First Class had the highest observed late-delivery rate**.

---

# 📉 Statistical Analysis

Statistical analysis was performed to understand distributions, relationships, outliers, confidence intervals, and differences between groups.

## Descriptive Statistics

### Sales

* Mean: **203.77**
* Median: **199.92**
* Standard deviation: **132.27**
* Variance: **17,496.17**

### Quantity

* Mean: **2.13**
* Median: **1**
* Standard deviation: **1.45**
* Variance: **2.11**

### Actual Delivery Duration

* Mean: **3.50 days**
* Median: **3 days**
* Standard deviation: **1.62**
* Variance: **2.64**

### Scheduled Delivery Duration

* Mean: **2.93 days**
* Median: **4 days**
* Standard deviation: **1.37**
* Variance: **1.89**

---

# 🔗 Correlation Analysis

The project analyzed relationships between:

* Sales and quantity
* Sales and actual delivery duration
* Sales and scheduled delivery duration
* Quantity and delivery duration
* Actual delivery duration and scheduled delivery duration

The strongest observed relationship was between **actual and scheduled delivery duration**, with a correlation of approximately **0.516**.

---

# 🚨 Outlier Analysis

Outliers were analyzed using:

* IQR method
* Z-score method

The main variable showing meaningful outliers was **Sales**.

### IQR Method

* Sales outliers: **488**

### Z-score Method

* Sales outliers: **467**

Other analyzed numerical variables did not show significant outlier counts using these methods.

---

# 📐 Confidence Interval

A 95% confidence interval was calculated for the mean actual delivery duration.

```text
Mean = 3.50 days

95% Confidence Interval:
3.49 – 3.51 days
```

---

# 🧪 Hypothesis Testing

An ANOVA test was performed to examine whether average delivery duration differs across shipping modes.

### Result

```text
F-statistic = 38,762.4138
p-value ≈ 0
```

The result indicates a statistically significant difference in delivery duration among the analyzed shipping modes.

Average actual delivery durations were approximately:

| Shipping Mode  | Average Delivery |
| -------------- | ---------------: |
| First Class    |        2.00 days |
| Same Day       |        0.48 days |
| Second Class   |        3.99 days |
| Standard Class |        4.00 days |

---

# 🔮 Demand Forecasting

Demand forecasting was performed using **monthly sales data**.

## Dataset

* Monthly observations: **37**
* Training observations: **30**
* Testing observations: **7**
* Future forecast horizon: **6 months**

## Models Compared

Two baseline forecasting approaches were compared:

1. Naive Baseline
2. Seasonal Naive

---

## Naive Baseline

| Metric |      Value |
| ------ | ---------: |
| MAE    | 131,973.37 |
| RMSE   | 191,232.60 |
| MAPE   |     23.45% |

---

## Seasonal Naive

| Metric |      Value |
| ------ | ---------: |
| MAE    | 277,036.77 |
| RMSE   | 373,534.00 |
| MAPE   |     58.43% |

### Selected Model

The **Naive Baseline** was selected because it produced lower:

* MAE
* RMSE
* MAPE

The selected model uses the latest observed monthly demand as the baseline for future demand planning.

### Business Applications

The forecast can support:

* Demand planning
* Inventory planning
* Logistics capacity planning
* Replenishment planning

### Forecast Limitation

The dataset does **not contain actual inventory stock levels**.

Therefore, the forecasting component is a **demand-planning indicator** and must not be interpreted as an actual stock-out prediction.

---

# 🤖 Late Delivery Prediction

A Machine Learning model was developed to predict:

```text
Late_delivery_risk
```

The objective is to identify whether an order is likely to experience late delivery using information available for prediction.

---

# 🧠 Machine Learning Features

The model uses:

* Days for shipment (scheduled)
* Shipping Mode
* Market
* Order Region
* Category Name
* Sales
* Order Item Quantity
* Product Price

Actual delivery outcomes were not used as predictive features in order to reduce target leakage.

---

# 🌲 Machine Learning Model

The selected model is:

**Random Forest Classifier**

### Dataset Split

| Dataset  | Samples |
| -------- | ------: |
| Training | 144,415 |
| Testing  |  36,104 |

---

# 📊 ML Performance

| Metric                  | Result |
| ----------------------- | -----: |
| Random Forest Accuracy  | 68.73% |
| Majority-Class Baseline | 54.83% |

The Random Forest model provides additional predictive information compared with the majority-class baseline.

### Confusion Matrix

```text
[[13521, 2787],
 [ 8501,11295]]
```

### Classification Performance

| Class   | Precision | Recall | F1-score |
| ------- | --------: | -----: | -------: |
| On-Time |      0.61 |   0.83 |     0.71 |
| Late    |      0.80 |   0.57 |     0.67 |

---

# ⭐ Feature Importance

Feature importance analysis was performed to identify the variables contributing most to late-delivery predictions.

The feature-importance results are stored in:

```text
data/processed/feature_importance.csv
```

These results are also visualized in the Power BI dashboard under:

**ML Insights → Top Features Affecting Late Delivery Risk**

Feature importance is interpreted as model-level predictive contribution and should not be treated as proof of direct causation.

---

# 🌍 Regional Logistics Risk Analysis

Regional logistics risk analysis was implemented as an additional analytical component.

For each region, the analysis considers:

* Sales
* Units
* Distinct orders
* Late-delivery rate
* Average delivery duration

Regions are categorized into:

* High Risk
* Medium Risk
* Low Risk

The classification is based on percentile-based thresholds for late-delivery rate and delivery duration.

### Output

The regional risk analysis generates:

```text
region_risk_analysis.csv
```

and a visualization:

```text
regional_late_delivery_rate.png
```

This analysis is intended as a logistics-monitoring indicator rather than a definitive operational risk classification.

---

# 📊 Power BI Dashboard

Power BI is the primary business-intelligence visualization layer of the project.

The dashboard contains multiple pages for executive, sales, logistics, demand, and machine-learning insights.

---

## Page 1 — Supply Chain Dashboard

The executive dashboard includes:

* Total Sales
* Total Orders
* Total Units Sold
* Sales by Category
* Sales by Shipping Mode
* Late Delivery Risk by Shipping Mode
* Delivery Status Distribution
* Sales by Region

This page provides a high-level overview of supply-chain performance.

---

# Page 2 — Demand & ML Insights

The second dashboard page includes analytical visuals such as:

* Historical Sales Trend
* Sales by Region
* Sales by Product
* Average Delivery Time by Shipping Mode
* Late Delivery Rate by Market
* Profit by Category
* Sales by Order Date
* Demand Forecast
* ML Feature Importance

The demand forecast uses the selected forecasting output rather than an automatically extended Power BI forecast.

---

# 📱 Streamlit Dashboard

A Streamlit dashboard is also included as an interactive analytical interface.

The application is located at:

```text
dashboard/app.py
```

The Streamlit application connects to:

```text
supply_chain.db
```

### Run Streamlit

```bash
streamlit run dashboard/app.py
```

The application normally opens at:

```text
http://localhost:8501
```

Streamlit provides an additional interactive interface for exploring the supply-chain analytics.

---

# 🚀 FastAPI

A FastAPI layer was implemented to expose selected project functionality through APIs.

The API is located at:

```text
api/app.py
```

## Available Endpoints

### Home

```http
GET /
```

### Late Delivery Prediction

```http
POST /predict-delay
```

### Product Information

```http
GET /product/{product_id}
```

### Regional Information

```http
GET /region/{region}
```

---

# ▶️ Running FastAPI

Run:

```bash
uvicorn api.app:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

FastAPI is an additional project component and is not required for the core analytics workflow.

---

# 🧠 GenAI Supply Chain Assistant

A GenAI-based assistant was implemented as an additional project component.

The assistant is located at:

```text
genai/assistant.py
```

The assistant uses a language model together with validated project information.

It can provide answers related to:

* Total sales
* Total profit
* Total orders
* Total customers
* Total products
* Late-delivery rate
* On-time rate
* ML accuracy
* Forecast MAE
* Forecast RMSE
* Inventory limitations
* Supplier-data limitations
* Supply-chain insights

The assistant follows a validated-answer approach so that numerical responses are based on known project results rather than invented values.

---

# 👷 Supplier Analysis Limitation

The dataset does not contain a proper supplier table or reliable supplier-level fields sufficient for comprehensive supplier-performance analysis.

Therefore:

* Supplier metrics were not artificially created.
* No unsupported supplier performance claims are made.
* Supplier analysis is identified as a dataset limitation.

This follows the principle of **not inventing unavailable business data**.

---

# 📦 Inventory Analysis Limitation

The dataset does not contain actual inventory quantities or stock-on-hand information.

Therefore, the project uses:

* Demand history
* Product movement
* Demand variability
* Forecasted demand

to provide **demand-based inventory planning indicators**.

The project does not claim to calculate actual:

* Stock levels
* Stock-outs
* Reorder points based on physical inventory
* Warehouse inventory quantities

without the required inventory data.

---

# 🗺️ Project Structure

```text
Supply_Chain_Project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── output files
│
├── notebooks/
│   ├── 01_data_understanding.py
│   ├── 02_data_quality.py
│   ├── 03_data_cleaning.py
│   ├── 04_eda.py
│   ├── 04_verify_cleaned_data.py
│   ├── 05_ml_preparation.py
│   ├── 06_train_model.py
│   ├── 07_feature_importance.py
│   ├── 08_prediction.py
│   ├── 09_model_evaluation.py
│   ├── 10_final_model.py
│   ├── 11_demand_forecasting.py
│   ├── 12_statistics_analysis.py
│   └── 13_route_region_risk.py
│
├── sql/
│   ├── 01_basic_queries.sql
│   ├── load_data.py
│   └── run_queries.py
│
├── dashboard/
│   └── app.py
│
├── api/
│   └── app.py
│
├── genai/
│   └── assistant.py
│
├── models/
│   ├── feature_names.pkl
│   └── late_delivery_model.pkl
│
├── supply_chain.db
├── requirements.txt
└── README.md
```

---

# ⚙️ Technologies Used

### Programming & Data Analysis

* Python
* Pandas
* NumPy

### Visualization

* Matplotlib
* Power BI
* Streamlit

### SQL

* SQLite
* SQL

### Statistics

* SciPy
* Statistical analysis
* ANOVA
* Correlation analysis
* Confidence intervals
* Outlier detection

### Machine Learning

* Scikit-learn
* Random Forest
* Feature importance
* Classification evaluation

### Forecasting

* Statsmodels
* Naive forecasting
* Seasonal Naive forecasting

### API

* FastAPI
* Uvicorn

### GenAI

* Transformers
* FLAN-T5
* PyTorch

### Development & Version Control

* Git
* GitHub
* VS Code

---

# 📂 Important Output Files

The project generates and uses several analytical outputs.

Examples include:

```text
data/processed/feature_importance.csv
data/processed/monthly_demand.csv
data/processed/demand_forecast.csv
data/processed/demand_forecast_evaluation.csv
data/processed/region_risk_analysis.csv
data/processed/regional_late_delivery_rate.png
```

The exact output location may depend on the execution configuration of individual analysis scripts.

---

# ▶️ How to Run the Project

## 1. Clone the Repository

```bash
git clone https://github.com/anushakesana20/Supply_Chain_Logistics_Intelligence.git
```

```bash
cd Supply_Chain_Logistics_Intelligence
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Run Data Understanding

```bash
python notebooks/01_data_understanding.py
```

---

## 4. Run Data Quality Analysis

```bash
python notebooks/02_data_quality.py
```

---

## 5. Run Data Cleaning

```bash
python notebooks/03_data_cleaning.py
```

---

## 6. Verify Cleaned Data

```bash
python notebooks/04_verify_cleaned_data.py
```

---

## 7. Load Data into SQLite

```bash
python sql/load_data.py
```

This creates/updates:

```text
supply_chain.db
```

---

## 8. Run SQL Analysis

```bash
python sql/run_queries.py
```

---

## 9. Run EDA

```bash
python notebooks/04_eda.py
```

---

## 10. Prepare ML Data

```bash
python notebooks/05_ml_preparation.py
```

---

## 11. Train ML Model

```bash
python notebooks/06_train_model.py
```

---

## 12. Generate Feature Importance

```bash
python notebooks/07_feature_importance.py
```

---

## 13. Run Prediction

```bash
python notebooks/08_prediction.py
```

---

## 14. Evaluate Model

```bash
python notebooks/09_model_evaluation.py
```

---

## 15. Generate Final Model Results

```bash
python notebooks/10_final_model.py
```

---

## 16. Run Demand Forecasting

```bash
python notebooks/11_demand_forecasting.py
```

---

## 17. Run Statistical Analysis

```bash
python notebooks/12_statistics_analysis.py
```

---

## 18. Run Regional Risk Analysis

```bash
python notebooks/13_route_region_risk.py
```

---

## 19. Run Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 20. Run FastAPI

```bash
uvicorn api.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# 📊 Business Value

The system can support supply-chain decision-making in several areas.

### Sales

Identify:

* High-performing categories
* High-performing products
* Regional sales performance
* Customer segment performance

### Logistics

Identify:

* High-risk shipping modes
* Late-delivery patterns
* Regional delivery issues
* Average delivery duration

### Demand Planning

Use demand forecasts to support:

* Future demand planning
* Inventory planning
* Replenishment planning
* Logistics capacity planning

### Machine Learning

Predict:

* Potential late-delivery risk

and identify important predictive features.

### Management

Power BI and Streamlit dashboards provide a centralized view of:

* Sales
* Profit
* Orders
* Units
* Delivery
* Logistics
* Demand
* ML insights

---

# ⚠️ Project Limitations

The following limitations should be considered when interpreting the results:

1. The dataset is an order-item-level dataset, not a complete real-time supply-chain system.
2. The dataset does not contain actual inventory quantities.
3. Therefore, actual stock-out prediction is not possible.
4. A complete supplier-performance analysis is not possible because reliable supplier-level data is unavailable.
5. Forecasting is based on historical sales rather than real-time market demand.
6. The selected forecasting model is a baseline model.
7. ML accuracy is dataset-dependent and should not be interpreted as guaranteed real-world prediction accuracy.
8. Feature importance indicates predictive contribution, not causation.
9. Regional risk categories are analytical indicators based on the project's percentile thresholds.
10. The project does not include real-time IoT, GPS, warehouse, or transportation-system data.

---

# 🔐 Data & Analytical Integrity

The project follows these principles:

* Do not count order-item rows directly as orders.
* Use distinct Order IDs for order-level calculations.
* Avoid target leakage in ML.
* Do not invent supplier information.
* Do not claim actual inventory levels without inventory data.
* Do not treat demand forecasts as actual stock-out predictions.
* Use validated project values for GenAI responses.
* Clearly document analytical limitations.

---

# 📌 Final Deliverables

The completed project provides:

* ✅ Cleaned and validated dataset
* ✅ Data-quality analysis
* ✅ SQLite analytical database
* ✅ SQL business analysis
* ✅ Exploratory Data Analysis
* ✅ KPI analysis
* ✅ Statistical analysis
* ✅ Correlation analysis
* ✅ Outlier analysis
* ✅ Hypothesis testing
* ✅ Demand forecasting
* ✅ Forecast evaluation
* ✅ Late-delivery ML model
* ✅ ML evaluation
* ✅ Confusion matrix
* ✅ Feature importance
* ✅ Regional logistics risk analysis
* ✅ Power BI dashboard
* ✅ Streamlit dashboard
* ✅ FastAPI prediction service
* ✅ GenAI supply-chain assistant
* ✅ GitHub repository
* ✅ Documentation of limitations

---

# 🏁 Conclusion

The **Supply Chain & Logistics Intelligence System** demonstrates how data analytics, SQL, statistics, forecasting, machine learning, business intelligence, APIs, and GenAI can be combined to analyze supply-chain operations.

The project transforms raw order-item data into:

```text
Data
 ↓
Information
 ↓
Business Insights
 ↓
Forecasts
 ↓
Risk Predictions
 ↓
Decision Support
```

The system can help organizations understand sales performance, monitor logistics and delivery issues, identify late-delivery risk, analyze demand patterns, and support future planning.

---

# 👩‍💻 Project Repository

GitHub:

https://github.com/anushakesana20/Supply_Chain_Logistics_Intelligence

---

## 📜 Disclaimer

This project is developed for **academic and analytical purposes** using the DataCo Smart Supply Chain Dataset.

The results and predictions are based on the available dataset and should be validated with real-time operational data before being used for production decision-making.
