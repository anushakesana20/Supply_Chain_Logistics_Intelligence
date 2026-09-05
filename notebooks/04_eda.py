import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv(
    "data/processed/DataCoSupplyChain_Cleaned.csv",
    encoding="utf-8"
)

print("Dataset shape:", df.shape)

# ==========================================
# 1. Delivery Status
# ==========================================

delivery_counts = df["Delivery Status"].value_counts()

delivery_counts.plot(kind="bar")

plt.title("Delivery Status Distribution")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Records")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ==========================================
# 2. Shipping Mode
# ==========================================

shipping_counts = df["Shipping Mode"].value_counts()

shipping_counts.plot(kind="bar")

plt.title("Shipping Mode Distribution")
plt.xlabel("Shipping Mode")
plt.ylabel("Number of Records")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ==========================================
# 3. Sales by Category - Top 10
# ==========================================

category_sales = (
    df.groupby("Category Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

category_sales.plot(kind="bar")

plt.title("Top 10 Categories by Sales")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ==========================================
# 4. Sales by Region - Top 10
# ==========================================

region_sales = (
    df.groupby("Order Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

region_sales.plot(kind="bar")

plt.title("Top 10 Regions by Sales")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


print("\nEDA completed successfully!")