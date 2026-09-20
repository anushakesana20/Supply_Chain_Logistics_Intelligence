import pandas as pd
import numpy as np
from scipy import stats

# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

file_path = "data/processed/DataCoSupplyChain_Cleaned.csv"

df = pd.read_csv(file_path, low_memory=False)

print("=" * 70)
print("SUPPLY CHAIN STATISTICS ANALYSIS")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ============================================================
# 2. DESCRIPTIVE STATISTICS
# ============================================================

numeric_columns = [
    "Sales",
    "Order Item Quantity",
    "Days for shipping (real)",
    "Days for shipment (scheduled)"
]

available_numeric = [
    col for col in numeric_columns
    if col in df.columns
]

print("\n" + "=" * 70)
print("1. DESCRIPTIVE STATISTICS")
print("=" * 70)

print(
    df[available_numeric]
    .describe()
    .round(2)
)


# ============================================================
# 3. ADDITIONAL STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("2. ADDITIONAL STATISTICS")
print("=" * 70)

for column in available_numeric:

    print(f"\n{column}")

    print(f"Mean       : {df[column].mean():.2f}")
    print(f"Median     : {df[column].median():.2f}")
    print(f"Std Dev    : {df[column].std():.2f}")
    print(f"Variance   : {df[column].var():.2f}")


# ============================================================
# 4. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("3. CORRELATION MATRIX")
print("=" * 70)

correlation_matrix = df[available_numeric].corr()

print(
    correlation_matrix.round(3)
)


# ============================================================
# 5. IQR OUTLIER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("4. IQR OUTLIER ANALYSIS")
print("=" * 70)

for column in available_numeric:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_limit) |
        (df[column] > upper_limit)
    ]

    print(f"\n{column}")

    print(f"Q1            : {Q1:.2f}")
    print(f"Q3            : {Q3:.2f}")
    print(f"IQR           : {IQR:.2f}")
    print(f"Lower Limit   : {lower_limit:.2f}")
    print(f"Upper Limit   : {upper_limit:.2f}")
    print(f"Outlier Count : {len(outliers)}")


# ============================================================
# 6. Z-SCORE OUTLIER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("5. Z-SCORE OUTLIER ANALYSIS")
print("=" * 70)

for column in available_numeric:

    values = df[column].dropna()

    z_scores = np.abs(stats.zscore(values))

    outlier_count = np.sum(z_scores > 3)

    print(
        f"{column}: "
        f"{outlier_count} observations with |Z| > 3"
    )


# ============================================================
# 7. 95% CONFIDENCE INTERVAL
#    FOR ACTUAL DELIVERY TIME
# ============================================================

print("\n" + "=" * 70)
print("6. 95% CONFIDENCE INTERVAL - DELIVERY TIME")
print("=" * 70)

delivery_column = "Days for shipping (real)"

delivery = df[delivery_column].dropna()

mean_delivery = delivery.mean()

standard_error = stats.sem(delivery)

confidence_interval = stats.t.interval(
    confidence=0.95,
    df=len(delivery) - 1,
    loc=mean_delivery,
    scale=standard_error
)

print(f"Mean delivery time : {mean_delivery:.2f} days")

print(
    f"95% Confidence Interval : "
    f"{confidence_interval[0]:.2f} "
    f"to "
    f"{confidence_interval[1]:.2f} days"
)


# ============================================================
# 8. HYPOTHESIS TEST
#    SHIPPING MODE vs DELIVERY TIME
# ============================================================

print("\n" + "=" * 70)
print("7. HYPOTHESIS TEST")
print("SHIPPING MODE vs ACTUAL DELIVERY TIME")
print("=" * 70)

shipping_mode_groups = []

for mode in sorted(df["Shipping Mode"].dropna().unique()):

    delivery_times = df.loc[
        df["Shipping Mode"] == mode,
        delivery_column
    ].dropna()

    shipping_mode_groups.append(delivery_times)

    print(
        f"{mode}: "
        f"Mean delivery time = "
        f"{delivery_times.mean():.2f} days"
    )


# One-way ANOVA

f_statistic, p_value = stats.f_oneway(
    *shipping_mode_groups
)

print(f"\nF-statistic : {f_statistic:.4f}")
print(f"P-value     : {p_value:.6f}")


if p_value < 0.05:

    print(
        "\nConclusion: There is a statistically significant "
        "difference in actual delivery time among shipping modes."
    )

else:

    print(
        "\nConclusion: There is no statistically significant "
        "difference in actual delivery time among shipping modes."
    )


# ============================================================
# 9. BUSINESS INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("8. BUSINESS INTERPRETATION")
print("=" * 70)

print("""
1. Descriptive statistics summarize the central tendency
   and variation of important supply-chain variables.

2. Correlation analysis helps identify relationships between
   sales, order quantity and delivery duration.

3. IQR and Z-score methods identify unusual observations
   that may require further investigation.

4. The 95% confidence interval provides an estimated range
   for the average actual delivery time.

5. The hypothesis test checks whether actual delivery time
   differs significantly across shipping modes.

6. These statistical results can support logistics planning,
   delivery improvement and operational decision-making.

7. Shipping cost statistics are not included because the
   cleaned DataCo dataset does not contain a Shipping Cost
   column.
""")

print("=" * 70)
print("STATISTICS ANALYSIS COMPLETED")
print("=" * 70)