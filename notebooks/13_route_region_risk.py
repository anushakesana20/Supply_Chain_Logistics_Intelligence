import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Load cleaned dataset
# --------------------------------------------------

file_path = "data/processed/DataCoSupplyChain_Cleaned.csv"

data = pd.read_csv(file_path)

print("Dataset loaded successfully.")
print("Shape:", data.shape)


# --------------------------------------------------
# 2. Regional Logistics Risk Analysis
# --------------------------------------------------

region_analysis = (
    data.groupby("Order Region")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Units=("Order Item Quantity", "sum"),
        Total_Orders=("Order Id", "nunique"),
        Late_Delivery_Rate=("Late_delivery_risk", "mean"),
        Average_Delivery_Days=("Days for shipping (real)", "mean")
    )
    .reset_index()
)

# Convert late rate to percentage
region_analysis["Late_Delivery_Rate"] = (
    region_analysis["Late_Delivery_Rate"] * 100
)

# Round values
region_analysis["Total_Sales"] = region_analysis["Total_Sales"].round(2)
region_analysis["Late_Delivery_Rate"] = (
    region_analysis["Late_Delivery_Rate"].round(2)
)
region_analysis["Average_Delivery_Days"] = (
    region_analysis["Average_Delivery_Days"].round(2)
)


# --------------------------------------------------
# 3. Create Risk Categories
# --------------------------------------------------

late_threshold = region_analysis["Late_Delivery_Rate"].quantile(0.75)
delivery_threshold = region_analysis["Average_Delivery_Days"].quantile(0.75)

def assign_risk(row):

    high_late = row["Late_Delivery_Rate"] >= late_threshold
    high_delivery = row["Average_Delivery_Days"] >= delivery_threshold

    if high_late and high_delivery:
        return "High Risk"

    elif high_late or high_delivery:
        return "Medium Risk"

    else:
        return "Low Risk"


region_analysis["Risk_Category"] = region_analysis.apply(
    assign_risk,
    axis=1
)


# --------------------------------------------------
# 4. Display Results
# --------------------------------------------------

print("\nREGIONAL LOGISTICS RISK ANALYSIS")
print("--------------------------------")

print(region_analysis.to_string(index=False))


print("\nRisk thresholds:")
print(
    "Late delivery rate threshold:",
    round(late_threshold, 2),
    "%"
)

print(
    "Average delivery days threshold:",
    round(delivery_threshold, 2),
    "days"
)


# --------------------------------------------------
# 5. Save Results
# --------------------------------------------------

output_file = "data/processed/region_risk_analysis.csv"

region_analysis.to_csv(
    output_file,
    index=False
)

print("\nSaved:", output_file)


# --------------------------------------------------
# 6. Visualize Late Delivery Rate by Region
# --------------------------------------------------

plot_data = region_analysis.sort_values(
    "Late_Delivery_Rate",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    plot_data["Order Region"],
    plot_data["Late_Delivery_Rate"]
)

plt.xlabel("Late Delivery Rate (%)")
plt.ylabel("Order Region")
plt.title("Late Delivery Rate by Region")

plt.tight_layout()

plt.savefig(
    "data/processed/regional_late_delivery_rate.png",
    dpi=300
)

plt.show()


print("\nRegional risk analysis completed successfully.")