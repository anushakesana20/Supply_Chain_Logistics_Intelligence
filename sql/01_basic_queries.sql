-- 1. Total records
SELECT COUNT(*) AS total_records
FROM supply_chain;


-- 2. Total unique orders
SELECT COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain;


-- 3. Total unique customers
SELECT COUNT(DISTINCT "Customer Id") AS total_customers
FROM supply_chain;


-- 4. Total unique products
SELECT COUNT(DISTINCT "Product Name") AS total_products
FROM supply_chain;


-- 5. Order status distribution
SELECT
    "Order Status",
    COUNT(*) AS record_count
FROM supply_chain
GROUP BY "Order Status"
ORDER BY record_count DESC;


-- 6. Shipping mode distribution
SELECT
    "Shipping Mode",
    COUNT(*) AS record_count
FROM supply_chain
GROUP BY "Shipping Mode"
ORDER BY record_count DESC;


-- 7. Delivery status distribution
SELECT
    "Delivery Status",
    COUNT(*) AS record_count
FROM supply_chain
GROUP BY "Delivery Status"
ORDER BY record_count DESC;
-- 8. Order status analysis
SELECT
    "Order Status",
    COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain
GROUP BY "Order Status"
ORDER BY total_orders DESC;
-- 8. Total Sales
SELECT
    SUM(Sales) AS total_sales
FROM supply_chain;


-- 9. Total Profit
SELECT
    SUM("Order Profit Per Order") AS total_profit
FROM supply_chain;


-- 10. Sales by Category
SELECT
    "Category Name",
    SUM(Sales) AS total_sales
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_sales DESC;


-- 11. Profit by Category
SELECT
    "Category Name",
    SUM("Order Profit Per Order") AS total_profit
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_profit DESC;


-- 12. Sales by Region
SELECT
    "Order Region",
    SUM(Sales) AS total_sales
FROM supply_chain
GROUP BY "Order Region"
ORDER BY total_sales DESC;
-- 13. Late delivery percentage by shipping mode
SELECT
    "Shipping Mode",
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN Late_delivery_risk = 1 THEN 1 ELSE 0 END) AS late_shipments,
    ROUND(
        100.0 * SUM(CASE WHEN Late_delivery_risk = 1 THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS late_percentage
FROM supply_chain
GROUP BY "Shipping Mode"
ORDER BY late_percentage DESC;


-- 14. Late delivery percentage by region
SELECT
    "Order Region",
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN Late_delivery_risk = 1 THEN 1 ELSE 0 END) AS late_shipments,
    ROUND(
        100.0 * SUM(CASE WHEN Late_delivery_risk = 1 THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS late_percentage
FROM supply_chain
GROUP BY "Order Region"
ORDER BY late_percentage DESC;


-- 15. Late delivery percentage by market
SELECT
    Market,
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN Late_delivery_risk = 1 THEN 1 ELSE 0 END) AS late_shipments,
    ROUND(
        100.0 * SUM(CASE WHEN Late_delivery_risk = 1 THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS late_percentage
FROM supply_chain
GROUP BY Market
ORDER BY late_percentage DESC;