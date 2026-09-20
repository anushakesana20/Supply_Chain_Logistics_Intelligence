import sqlite3

# Connect to database
connection = sqlite3.connect("supply_chain.db")
cursor = connection.cursor()


# ==========================================
# BASIC INFORMATION
# ==========================================

print("\n========== BASIC INFORMATION ==========")

cursor.execute("""
SELECT COUNT(*)
FROM supply_chain
""")
print("Total records:", cursor.fetchone()[0])

cursor.execute("""
SELECT COUNT(DISTINCT "Order Id")
FROM supply_chain
""")
print("Total unique orders:", cursor.fetchone()[0])

cursor.execute("""
SELECT COUNT(DISTINCT "Customer Id")
FROM supply_chain
""")
print("Total unique customers:", cursor.fetchone()[0])

cursor.execute("""
SELECT COUNT(DISTINCT "Product Name")
FROM supply_chain
""")
print("Total unique products:", cursor.fetchone()[0])


# ==========================================
# ORDER STATUS
# ==========================================

print("\n========== ORDER STATUS ==========")

cursor.execute("""
SELECT
    "Order Status",
    COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain
GROUP BY "Order Status"
ORDER BY total_orders DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# SHIPPING MODE
# ==========================================

print("\n========== SHIPPING MODE ==========")

cursor.execute("""
SELECT
    "Shipping Mode",
    COUNT(*) AS record_count
FROM supply_chain
GROUP BY "Shipping Mode"
ORDER BY record_count DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# DELIVERY STATUS
# ==========================================

print("\n========== DELIVERY STATUS ==========")

cursor.execute("""
SELECT
    "Delivery Status",
    COUNT(*) AS record_count
FROM supply_chain
GROUP BY "Delivery Status"
ORDER BY record_count DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# TOTAL SALES
# ==========================================

print("\n========== TOTAL SALES ==========")

cursor.execute("""
SELECT SUM(Sales)
FROM supply_chain
""")

print("Total sales:", cursor.fetchone()[0])


# ==========================================
# TOTAL PROFIT
# ==========================================

print("\n========== TOTAL PROFIT ==========")

cursor.execute("""
SELECT SUM("Order Profit Per Order")
FROM supply_chain
""")

print("Total profit:", cursor.fetchone()[0])


# ==========================================
# SALES BY CATEGORY
# ==========================================

print("\n========== SALES BY CATEGORY ==========")

cursor.execute("""
SELECT
    "Category Name",
    SUM(Sales) AS total_sales
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_sales DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# PROFIT BY CATEGORY
# ==========================================

print("\n========== PROFIT BY CATEGORY ==========")

cursor.execute("""
SELECT
    "Category Name",
    SUM("Order Profit Per Order") AS total_profit
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_profit DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# SALES BY REGION
# ==========================================

print("\n========== SALES BY REGION ==========")

cursor.execute("""
SELECT
    "Order Region",
    SUM(Sales) AS total_sales
FROM supply_chain
GROUP BY "Order Region"
ORDER BY total_sales DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# LATE DELIVERY BY SHIPPING MODE
# ==========================================

print("\n========== LATE DELIVERY BY SHIPPING MODE ==========")

cursor.execute("""
SELECT
    "Shipping Mode",
    COUNT(*) AS total_shipments,
    SUM(
        CASE
            WHEN Late_delivery_risk = 1 THEN 1
            ELSE 0
        END
    ) AS late_shipments,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Late_delivery_risk = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_percentage
FROM supply_chain
GROUP BY "Shipping Mode"
ORDER BY late_percentage DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# LATE DELIVERY BY REGION
# ==========================================

print("\n========== LATE DELIVERY BY REGION ==========")

cursor.execute("""
SELECT
    "Order Region",
    COUNT(*) AS total_shipments,
    SUM(
        CASE
            WHEN Late_delivery_risk = 1 THEN 1
            ELSE 0
        END
    ) AS late_shipments,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Late_delivery_risk = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_percentage
FROM supply_chain
GROUP BY "Order Region"
ORDER BY late_percentage DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# LATE DELIVERY BY MARKET
# ==========================================

print("\n========== LATE DELIVERY BY MARKET ==========")

cursor.execute("""
SELECT
    Market,
    COUNT(*) AS total_shipments,
    SUM(
        CASE
            WHEN Late_delivery_risk = 1 THEN 1
            ELSE 0
        END
    ) AS late_shipments,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Late_delivery_risk = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_percentage
FROM supply_chain
GROUP BY Market
ORDER BY late_percentage DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# TOTAL UNITS SOLD
# ==========================================

print("\n========== TOTAL UNITS SOLD ==========")

cursor.execute("""
SELECT
    SUM("Order Item Quantity")
FROM supply_chain
""")

print("Total units sold:", cursor.fetchone()[0])


# ==========================================
# AVERAGE ORDER VALUE
# ==========================================

print("\n========== AVERAGE ORDER VALUE ==========")

cursor.execute("""
SELECT
    ROUND(
        SUM(Sales) / COUNT(DISTINCT "Order Id"),
        2
    )
FROM supply_chain
""")

print("Average order value:", cursor.fetchone()[0])


# ==========================================
# AVERAGE DELIVERY DURATION
# ==========================================

print("\n========== AVERAGE DELIVERY DURATION ==========")

cursor.execute("""
SELECT
    ROUND(
        AVG("Days for shipping (real)"),
        2
    )
FROM supply_chain
""")

print("Average delivery duration:",
      cursor.fetchone()[0], "days")


# ==========================================
# ON-TIME DELIVERY RATE
# ==========================================

print("\n========== ON-TIME DELIVERY RATE ==========")

cursor.execute("""
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Late_delivery_risk = 0 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    )
FROM supply_chain
""")

print("On-time delivery rate:",
      cursor.fetchone()[0], "%")


# ==========================================
# LATE DELIVERY RATE
# ==========================================

print("\n========== LATE DELIVERY RATE ==========")

cursor.execute("""
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Late_delivery_risk = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    )
FROM supply_chain
""")

print("Late delivery rate:",
      cursor.fetchone()[0], "%")


# ==========================================
# SALES BY CUSTOMER SEGMENT
# ==========================================

print("\n========== SALES BY CUSTOMER SEGMENT ==========")

cursor.execute("""
SELECT
    "Customer Segment",
    SUM(Sales) AS total_sales,
    COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain
GROUP BY "Customer Segment"
ORDER BY total_sales DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# TOP 10 PRODUCTS BY SALES
# ==========================================

print("\n========== TOP 10 PRODUCTS BY SALES ==========")

cursor.execute("""
SELECT
    "Product Name",
    SUM(Sales) AS total_sales,
    SUM("Order Item Quantity") AS units_sold
FROM supply_chain
GROUP BY "Product Name"
ORDER BY total_sales DESC
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# TOP 10 REGIONS BY SALES
# ==========================================

print("\n========== TOP 10 REGIONS BY SALES ==========")

cursor.execute("""
SELECT
    "Order Region",
    SUM(Sales) AS total_sales,
    COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain
GROUP BY "Order Region"
ORDER BY total_sales DESC
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# MONTHLY SALES
# ==========================================

print("\n========== MONTHLY SALES ==========")

cursor.execute("""
SELECT
    strftime(
        '%Y-%m',
        "order date (DateOrders)"
    ) AS month,
    ROUND(SUM(Sales), 2) AS monthly_sales
FROM supply_chain
WHERE "order date (DateOrders)" IS NOT NULL
GROUP BY month
ORDER BY month
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# MONTH-OVER-MONTH SALES GROWTH
# ==========================================

print("\n========== MONTH-OVER-MONTH SALES GROWTH ==========")

cursor.execute("""
WITH monthly_sales AS (
    SELECT
        strftime(
            '%Y-%m',
            "order date (DateOrders)"
        ) AS month,
        SUM(Sales) AS sales
    FROM supply_chain
    WHERE "order date (DateOrders)" IS NOT NULL
    GROUP BY month
),

sales_with_previous AS (
    SELECT
        month,
        sales,
        LAG(sales) OVER (
            ORDER BY month
        ) AS previous_month_sales
    FROM monthly_sales
)

SELECT
    month,
    ROUND(sales, 2) AS sales,
    ROUND(previous_month_sales, 2)
        AS previous_month_sales,
    ROUND(
        100.0 * (sales - previous_month_sales)
        / NULLIF(previous_month_sales, 0),
        2
    ) AS mom_growth_percentage
FROM sales_with_previous
ORDER BY month
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# REGIONAL SALES RANKING
# ==========================================

print("\n========== REGIONAL SALES RANKING ==========")

cursor.execute("""
WITH regional_sales AS (
    SELECT
        "Order Region" AS region,
        SUM(Sales) AS total_sales
    FROM supply_chain
    GROUP BY "Order Region"
)

SELECT
    region,
    ROUND(total_sales, 2) AS total_sales,
    RANK() OVER (
        ORDER BY total_sales DESC
    ) AS sales_rank
FROM regional_sales
ORDER BY sales_rank
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# SHIPPING MODE PERFORMANCE
# ==========================================

print("\n========== SHIPPING MODE PERFORMANCE ==========")

cursor.execute("""
SELECT
    "Shipping Mode",
    COUNT(DISTINCT "Order Id") AS total_orders,
    ROUND(
        AVG("Days for shipping (real)"),
        2
    ) AS avg_delivery_days,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN "Late_delivery_risk" = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
GROUP BY "Shipping Mode"
ORDER BY late_delivery_percentage DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# HIGH-SALES PRODUCTS WITH DELIVERY ISSUES
# ==========================================

print("\n========== HIGH-SALES PRODUCTS WITH DELIVERY ISSUES ==========")

cursor.execute("""
SELECT
    "Product Name",
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN Late_delivery_risk = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Late_delivery_risk = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
GROUP BY "Product Name"
HAVING SUM(Sales) > (
    SELECT AVG(product_sales)
    FROM (
        SELECT
            "Product Name",
            SUM(Sales) AS product_sales
        FROM supply_chain
        GROUP BY "Product Name"
    )
)
ORDER BY total_sales DESC,
         late_delivery_percentage DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# MONTHLY REGIONAL SALES RANKING
# ==========================================

print("\n========== MONTHLY REGIONAL SALES RANKING ==========")

cursor.execute("""
WITH monthly_region_sales AS (
    SELECT
        strftime(
            '%Y-%m',
            "order date (DateOrders)"
        ) AS month,
        "Order Region" AS region,
        SUM(Sales) AS total_sales
    FROM supply_chain
    WHERE "order date (DateOrders)" IS NOT NULL
    GROUP BY month, region
),

ranked_regions AS (
    SELECT
        month,
        region,
        total_sales,
        RANK() OVER (
            PARTITION BY month
            ORDER BY total_sales DESC
        ) AS regional_rank
    FROM monthly_region_sales
)

SELECT
    month,
    region,
    ROUND(total_sales, 2) AS total_sales,
    regional_rank
FROM ranked_regions
ORDER BY month,
         regional_rank
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# INVENTORY & DEMAND ANALYTICS
# ==========================================

# ==========================================
# FAST-MOVING PRODUCTS
# ==========================================

print("\n========== FAST-MOVING PRODUCTS ==========")

cursor.execute("""
SELECT
    "Product Name",
    SUM("Order Item Quantity") AS units_sold,
    ROUND(SUM(Sales), 2) AS total_sales
FROM supply_chain
GROUP BY "Product Name"
ORDER BY units_sold DESC
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# SLOW-MOVING PRODUCTS
# ==========================================

print("\n========== SLOW-MOVING PRODUCTS ==========")

cursor.execute("""
SELECT
    "Product Name",
    SUM("Order Item Quantity") AS units_sold,
    ROUND(SUM(Sales), 2) AS total_sales
FROM supply_chain
GROUP BY "Product Name"
ORDER BY units_sold ASC
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# DEMAND BY MONTH
# ==========================================

print("\n========== DEMAND BY MONTH ==========")

cursor.execute("""
SELECT
    strftime(
        '%Y-%m',
        "order date (DateOrders)"
    ) AS month,
    SUM("Order Item Quantity") AS monthly_units
FROM supply_chain
WHERE "order date (DateOrders)" IS NOT NULL
GROUP BY month
ORDER BY month
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# DEMAND BY PRODUCT CATEGORY
# ==========================================

print("\n========== DEMAND BY PRODUCT CATEGORY ==========")

cursor.execute("""
SELECT
    "Category Name",
    SUM("Order Item Quantity") AS total_units,
    ROUND(
        AVG("Order Item Quantity"),
        2
    ) AS avg_quantity_per_record
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_units DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# DEMAND VARIABILITY BY PRODUCT
# ==========================================

print("\n========== DEMAND VARIABILITY BY PRODUCT ==========")

cursor.execute("""
SELECT
    "Product Name",
    COUNT(*) AS observations,
    ROUND(
        AVG("Order Item Quantity"),
        2
    ) AS avg_quantity,
    ROUND(
        AVG(
            "Order Item Quantity"
            * "Order Item Quantity"
        )
        - AVG("Order Item Quantity")
          * AVG("Order Item Quantity"),
        2
    ) AS quantity_variance
FROM supply_chain
GROUP BY "Product Name"
ORDER BY quantity_variance DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# DELIVERY PERFORMANCE BY CUSTOMER SEGMENT
# ==========================================

print("\n========== DELIVERY PERFORMANCE BY CUSTOMER SEGMENT ==========")

cursor.execute("""
SELECT
    "Customer Segment",
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN Late_delivery_risk = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Late_delivery_risk = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
GROUP BY "Customer Segment"
ORDER BY late_delivery_percentage DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# SALES AND DELIVERY ISSUES BY CATEGORY
# ==========================================

print("\n========== SALES AND DELIVERY ISSUES BY CATEGORY ==========")

cursor.execute("""
SELECT
    "Category Name",
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN Late_delivery_risk = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Late_delivery_risk = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_sales DESC
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# CUMULATIVE SALES BY MONTH
# ==========================================

print("\n========== CUMULATIVE SALES BY MONTH ==========")

cursor.execute("""
WITH monthly_sales AS (
    SELECT
        strftime(
            '%Y-%m',
            "order date (DateOrders)"
        ) AS month,
        SUM(Sales) AS monthly_sales
    FROM supply_chain
    WHERE "order date (DateOrders)" IS NOT NULL
    GROUP BY month
)

SELECT
    month,
    ROUND(monthly_sales, 2) AS monthly_sales,
    ROUND(
        SUM(monthly_sales) OVER (
            ORDER BY month
        ),
        2
    ) AS cumulative_sales
FROM monthly_sales
ORDER BY month
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# TOP PRODUCTS WITH LATE DELIVERY
# ==========================================

print("\n========== TOP PRODUCTS WITH LATE DELIVERY ==========")

cursor.execute("""
SELECT
    "Product Name",
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN Late_delivery_risk = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Late_delivery_risk = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_percentage,
    ROUND(SUM(Sales), 2) AS total_sales
FROM supply_chain
GROUP BY "Product Name"
HAVING SUM(
    CASE
        WHEN Late_delivery_risk = 1 THEN 1
        ELSE 0
    END
) > 0
ORDER BY late_percentage DESC
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# SALES BY YEAR
# ==========================================

print("\n========== SALES BY YEAR ==========")

cursor.execute("""
SELECT
    strftime(
        '%Y',
        "order date (DateOrders)"
    ) AS year,
    ROUND(SUM(Sales), 2) AS total_sales
FROM supply_chain
WHERE "order date (DateOrders)" IS NOT NULL
GROUP BY year
ORDER BY year
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# ORDERS BY YEAR
# ==========================================

print("\n========== ORDERS BY YEAR ==========")

cursor.execute("""
SELECT
    strftime(
        '%Y',
        "order date (DateOrders)"
    ) AS year,
    COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain
WHERE "order date (DateOrders)" IS NOT NULL
GROUP BY year
ORDER BY year
""")

for row in cursor.fetchall():
    print(row)


# ==========================================
# CLOSE DATABASE
# ==========================================

connection.close()

print("\n========== DONE ==========")