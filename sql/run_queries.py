import sqlite3

# Connect to database
connection = sqlite3.connect("supply_chain.db")
cursor = connection.cursor()


# ==========================================
# BASIC INFORMATION
# ==========================================

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
# CLOSE DATABASE
# ==========================================

connection.close()

print("\n========== DONE ==========")