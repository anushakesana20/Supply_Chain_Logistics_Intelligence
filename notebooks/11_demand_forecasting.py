import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ============================================================
# DEMAND FORECASTING - SUPPLY CHAIN PROJECT
# Naive Baseline + Seasonal Naive Forecasting
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
# NAIVE BASELINE MODEL
# ============================================================

print(
    "\n========== NAIVE BASELINE ==========\n"
)

print(
    "Using the previous month's sales as the baseline forecast..."
)


naive_forecast_values = []


for i in range(len(test)):

    if i == 0:

        value = train.iloc[-1]

    else:

        value = test.iloc[i - 1]

    naive_forecast_values.append(
        value
    )


naive_forecast = pd.Series(
    naive_forecast_values,
    index=test.index,
    name="Naive Forecast"
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


seasonal_forecast_values = []


for date in test.index:

    previous_year = date - pd.DateOffset(
        years=1
    )

    if previous_year in train.index:

        value = train.loc[
            previous_year
        ]

    else:

        value = train.iloc[-1]

    seasonal_forecast_values.append(
        value
    )


seasonal_forecast = pd.Series(
    seasonal_forecast_values,
    index=test.index,
    name="Seasonal Forecast"
)


print(
    "Seasonal forecast model trained successfully."
)


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def calculate_metrics(actual, forecast):

    mae = mean_absolute_error(
        actual,
        forecast
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            forecast
        )
    )

    actual_values = actual.to_numpy()

    forecast_values = forecast.to_numpy()

    non_zero_mask = (
        actual_values != 0
    )

    if non_zero_mask.sum() > 0:

        mape = (
            np.mean(
                np.abs(
                    (
                        actual_values[non_zero_mask]
                        -
                        forecast_values[non_zero_mask]
                    )
                    /
                    actual_values[non_zero_mask]
                )
            )
            * 100
        )

    else:

        mape = np.nan

    return mae, rmse, mape


# ============================================================
# CALCULATE BASELINE METRICS
# ============================================================

naive_mae, naive_rmse, naive_mape = calculate_metrics(
    test,
    naive_forecast
)


# ============================================================
# CALCULATE SEASONAL MODEL METRICS
# ============================================================

seasonal_mae, seasonal_rmse, seasonal_mape = calculate_metrics(
    test,
    seasonal_forecast
)


# ============================================================
# DISPLAY MODEL COMPARISON
# ============================================================

print(
    "\n========== MODEL COMPARISON ==========\n"
)


print(
    "Naive Baseline:"
)

print(
    f"MAE: {naive_mae:,.2f}"
)

print(
    f"RMSE: {naive_rmse:,.2f}"
)

if not np.isnan(naive_mape):

    print(
        f"MAPE: {naive_mape:.2f}%"
    )


print(
    "\nSeasonal Naive Model:"
)

print(
    f"MAE: {seasonal_mae:,.2f}"
)

print(
    f"RMSE: {seasonal_rmse:,.2f}"
)

if not np.isnan(seasonal_mape):

    print(
        f"MAPE: {seasonal_mape:.2f}%"
    )


# ============================================================
# DETERMINE BETTER MODEL
# ============================================================

if seasonal_mae < naive_mae:

    selected_model = "Seasonal Naive"

else:

    selected_model = "Naive Baseline"


print(
    "\nSelected forecasting approach:",
    selected_model
)


# ============================================================
# SAVE MODEL COMPARISON
# ============================================================

evaluation_results = pd.DataFrame({

    "Model": [
        "Naive Baseline",
        "Seasonal Naive"
    ],

    "MAE": [
        naive_mae,
        seasonal_mae
    ],

    "RMSE": [
        naive_rmse,
        seasonal_rmse
    ],

    "MAPE": [
        naive_mape,
        seasonal_mape
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
# FINAL FORECAST MODEL
# ============================================================

print(
    "\n========== FINAL FORECAST MODEL ==========\n"
)

print(
    "Generating next 6 months forecast using:",
    selected_model
)


FORECAST_MONTHS = 6


last_date = monthly_demand.index[-1]


future_dates = pd.date_range(
    start=last_date + pd.offsets.MonthEnd(1),
    periods=FORECAST_MONTHS,
    freq="ME"
)


future_values = []


# ============================================================
# GENERATE FUTURE FORECAST USING SELECTED MODEL
# ============================================================

for date in future_dates:

    if selected_model == "Naive Baseline":

        # For the first future month, use the last
        # historical value.
        #
        # For the next months, use the previous
        # forecasted value.

        if len(future_values) == 0:

            value = monthly_demand.iloc[-1]

        else:

            value = future_values[-1]

    else:

        # Seasonal Naive:
        # Use the same month from the previous year.

        previous_year = date - pd.DateOffset(
            years=1
        )

        if previous_year in monthly_demand.index:

            value = monthly_demand.loc[
                previous_year
            ]

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
# ACTUAL VS BASELINE VS SEASONAL FORECAST
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
    naive_forecast.values,
    marker="o",
    label="Naive Baseline"
)


plt.plot(
    test.index,
    seasonal_forecast.values,
    marker="o",
    label="Seasonal Naive Forecast"
)


plt.title(
    "Demand Forecasting - Model Comparison"
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
# BUSINESS INTERPRETATION
# ============================================================

print(
    "\n========== BUSINESS INTERPRETATION ==========\n"
)

print(
    "The forecast can be used to support inventory "
    "and demand planning."
)

print(
    "Higher forecasted sales indicate periods where "
    "additional inventory and logistics capacity "
    "may be required."
)

print(
    "Lower forecasted sales indicate periods where "
    "inventory replenishment can be controlled "
    "to reduce excess stock."
)

print(
    "Because the dataset does not contain actual "
    "inventory stock levels, the forecast is used "
    "as a demand-planning indicator rather than "
    "an actual stock-out prediction."
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