import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ============================================================
# DEMAND FORECASTING - SUPPLY CHAIN PROJECT
# Seasonal Naive Forecasting
# ============================================================

print("\n========== DEMAND FORECASTING ==========\n")


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "DataCoSupplyChainDataset.csv"

OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_csv(
    DATA_PATH,
    encoding="latin1"
)

print("Original shape:", df.shape)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

DATE_COLUMN = "order date (DateOrders)"
SALES_COLUMN = "Sales"


if DATE_COLUMN not in df.columns:

    print(
        f"\nERROR: Required column '{DATE_COLUMN}' not found."
    )

    print("\nAvailable columns:")
    print(df.columns.tolist())

    raise SystemExit


if SALES_COLUMN not in df.columns:

    print(
        f"\nERROR: Required column '{SALES_COLUMN}' not found."
    )

    raise SystemExit


# ============================================================
# DATE CONVERSION
# ============================================================

print("\nConverting order date...")

df[DATE_COLUMN] = pd.to_datetime(
    df[DATE_COLUMN],
    errors="coerce"
)


# ============================================================
# SALES CONVERSION
# ============================================================

print("Converting sales values...")

df[SALES_COLUMN] = pd.to_numeric(
    df[SALES_COLUMN],
    errors="coerce"
)


# ============================================================
# REMOVE INVALID RECORDS
# ============================================================

df = df.dropna(
    subset=[
        DATE_COLUMN,
        SALES_COLUMN
    ]
)

print(
    "Records after cleaning:",
    len(df)
)


# ============================================================
# CREATE MONTHLY SALES
# ============================================================

print("\nCreating monthly demand...")

monthly_demand = (
    df
    .set_index(DATE_COLUMN)
    .resample("ME")[SALES_COLUMN]
    .sum()
)


print("\n========== MONTHLY DEMAND ==========\n")

print(
    monthly_demand.to_string()
)


# ============================================================
# NUMBER OF MONTHS
# ============================================================

number_of_months = len(
    monthly_demand
)

print(
    "\nNumber of monthly observations:",
    number_of_months
)


if number_of_months < 24:

    print(
        "\nERROR: At least 24 months are required "
        "for seasonal forecasting."
    )

    raise SystemExit


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print(
    "\n========== TRAIN / TEST SPLIT ==========\n"
)


# Last 7 months used for testing

test_size = 7


train = monthly_demand.iloc[
    :-test_size
]

test = monthly_demand.iloc[
    -test_size:
]


print(
    "Training observations:",
    len(train)
)

print(
    "Testing observations:",
    len(test)
)

print(
    "Training period:",
    train.index.min().date(),
    "to",
    train.index.max().date()
)

print(
    "Testing period:",
    test.index.min().date(),
    "to",
    test.index.max().date()
)


# ============================================================
# SEASONAL NAIVE FORECAST
# ============================================================

print(
    "\n========== TRAINING FORECAST MODEL ==========\n"
)

print(
    "Using 12-month seasonal pattern..."
)


# For each test month, use the value
# from the same month in the previous year.

test_forecast_values = []

for date in test.index:

    previous_year = date - pd.DateOffset(years=1)

    if previous_year in train.index:

        value = train.loc[previous_year]

    else:

        value = train.iloc[-1]

    test_forecast_values.append(value)


test_forecast = pd.Series(
    test_forecast_values,
    index=test.index,
    name="Forecast"
)


print(
    "Forecast model trained successfully."
)


# ============================================================
# MODEL EVALUATION
# ============================================================

mae = mean_absolute_error(
    test,
    test_forecast
)


rmse = np.sqrt(
    mean_squared_error(
        test,
        test_forecast
    )
)


# Safe MAPE calculation

test_values = test.to_numpy()

forecast_values = test_forecast.to_numpy()


non_zero_mask = (
    test_values != 0
)


if non_zero_mask.sum() > 0:

    mape = (
        np.mean(
            np.abs(
                (
                    test_values[non_zero_mask]
                    -
                    forecast_values[non_zero_mask]
                )
                /
                test_values[non_zero_mask]
            )
        )
        * 100
    )

else:

    mape = np.nan


# ============================================================
# DISPLAY PERFORMANCE
# ============================================================

print(
    "\n========== FORECAST MODEL PERFORMANCE ==========\n"
)

print(
    f"Mean Absolute Error (MAE): {mae:,.2f}"
)

print(
    f"Root Mean Squared Error (RMSE): {rmse:,.2f}"
)

if not np.isnan(mape):

    print(
        f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%"
    )


# ============================================================
# SAVE EVALUATION RESULTS
# ============================================================

evaluation_results = pd.DataFrame({

    "Metric": [
        "MAE",
        "RMSE",
        "MAPE"
    ],

    "Value": [
        mae,
        rmse,
        mape
    ]

})


evaluation_path = (
    OUTPUT_DIR
    / "demand_forecast_evaluation.csv"
)


evaluation_results.to_csv(
    evaluation_path,
    index=False
)


print(
    "\nEvaluation results saved to:"
)

print(
    evaluation_path
)


# ============================================================
# FUTURE FORECAST - NEXT 6 MONTHS
# ============================================================

print(
    "\n========== FINAL FORECAST MODEL ==========\n"
)

print(
    "Generating next 6 months forecast..."
)


FORECAST_MONTHS = 6


last_date = monthly_demand.index[-1]


future_dates = pd.date_range(
    start=last_date + pd.offsets.MonthEnd(1),
    periods=FORECAST_MONTHS,
    freq="ME"
)


future_values = []


for date in future_dates:

    previous_year = date - pd.DateOffset(years=1)

    if previous_year in monthly_demand.index:

        value = monthly_demand.loc[previous_year]

    else:

        value = monthly_demand.iloc[-1]

    future_values.append(
        value
    )


future_forecast = pd.Series(
    future_values,
    index=future_dates,
    name="Forecasted Sales"
)


# Ensure sales cannot be negative

future_forecast = future_forecast.clip(
    lower=0
)


# ============================================================
# FORECAST TABLE
# ============================================================

forecast_table = pd.DataFrame({

    "Month": future_forecast.index,

    "Forecasted Sales": future_forecast.values

})


print(
    "\n========== NEXT 6 MONTHS FORECAST ==========\n"
)

print(
    forecast_table.to_string(
        index=False
    )
)


# ============================================================
# SAVE FORECAST
# ============================================================

forecast_path = (
    OUTPUT_DIR
    / "demand_forecast.csv"
)


forecast_table.to_csv(
    forecast_path,
    index=False
)


print(
    "\nForecast saved to:"
)

print(
    forecast_path
)


# ============================================================
# SAVE MONTHLY HISTORICAL DATA
# ============================================================

monthly_table = monthly_demand.reset_index()


monthly_table.columns = [
    "Month",
    "Sales"
]


monthly_path = (
    OUTPUT_DIR
    / "monthly_demand.csv"
)


monthly_table.to_csv(
    monthly_path,
    index=False
)


print(
    "\nMonthly demand data saved to:"
)

print(
    monthly_path
)


# ============================================================
# GRAPH 1
# ACTUAL VS FORECAST
# ============================================================

plt.figure(
    figsize=(12, 6)
)


plt.plot(
    train.index,
    train.values,
    label="Training Sales"
)


plt.plot(
    test.index,
    test.values,
    label="Actual Test Sales"
)


plt.plot(
    test.index,
    test_forecast.values,
    marker="o",
    label="Seasonal Forecast"
)


plt.title(
    "Demand Forecasting - Model Evaluation"
)

plt.xlabel(
    "Date"
)

plt.ylabel(
    "Sales"
)

plt.legend()

plt.tight_layout()


evaluation_graph_path = (
    OUTPUT_DIR
    / "demand_forecast_evaluation.png"
)


plt.savefig(
    evaluation_graph_path,
    dpi=150,
    bbox_inches="tight"
)

plt.close()


print(
    "\nEvaluation graph saved to:"
)

print(
    evaluation_graph_path
)


# ============================================================
# GRAPH 2
# HISTORICAL + FUTURE FORECAST
# ============================================================

plt.figure(
    figsize=(12, 6)
)


plt.plot(
    monthly_demand.index,
    monthly_demand.values,
    label="Historical Sales"
)


plt.plot(
    future_forecast.index,
    future_forecast.values,
    marker="o",
    label="Next 6 Months Forecast"
)


plt.title(
    "Demand Forecast - Next 6 Months"
)

plt.xlabel(
    "Date"
)

plt.ylabel(
    "Sales"
)

plt.legend()

plt.tight_layout()


future_graph_path = (
    OUTPUT_DIR
    / "demand_forecast_future.png"
)


plt.savefig(
    future_graph_path,
    dpi=150,
    bbox_inches="tight"
)

plt.close()


print(
    "Future forecast graph saved to:"
)

print(
    future_graph_path
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print(
    "\n=============================================="
)

print(
    "DEMAND FORECASTING COMPLETED SUCCESSFULLY"
)

print(
    "=============================================="
)

print(
    "\nFiles created:"
)

print(
    "1. demand_forecast.csv"
)

print(
    "2. demand_forecast_evaluation.csv"
)

print(
    "3. monthly_demand.csv"
)

print(
    "4. demand_forecast_evaluation.png"
)

print(
    "5. demand_forecast_future.png"
)

print(
    "\nForecasting step completed."
)