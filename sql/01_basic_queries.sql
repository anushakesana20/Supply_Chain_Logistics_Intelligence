-- ============================================================
-- SUPPLY CHAIN LOGISTICS INTELLIGENCE PROJECT
-- SQL BUSINESS & OPERATIONAL ANALYSIS
-- ============================================================


-- ============================================================
-- 1. TOTAL RECORDS
-- ============================================================

SELECT COUNT(*) AS total_records
FROM supply_chain;


-- ============================================================
-- 2. TOTAL UNIQUE ORDERS
-- ============================================================

SELECT COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain;


-- ============================================================
-- 3. TOTAL UNIQUE CUSTOMERS
-- ============================================================

SELECT COUNT(DISTINCT "Customer Id") AS total_customers
FROM supply_chain;


-- ============================================================
-- 4. TOTAL UNIQUE PRODUCTS
-- ============================================================

SELECT COUNT(DISTINCT "Product Card Id") AS total_products
FROM supply_chain;


-- ============================================================
-- 5. ORDER STATUS DISTRIBUTION
-- ============================================================

SELECT
    "Order Status",
    COUNT(*) AS record_count
FROM supply_chain
GROUP BY "Order Status"
ORDER BY record_count DESC;


-- ============================================================
-- 6. SHIPPING MODE DISTRIBUTION
-- ============================================================

SELECT
    "Shipping Mode",
    COUNT(*) AS record_count
FROM supply_chain
GROUP BY "Shipping Mode"
ORDER BY record_count DESC;


-- ============================================================
-- 7. DELIVERY STATUS DISTRIBUTION
-- ============================================================

SELECT
    "Delivery Status",
    COUNT(*) AS record_count
FROM supply_chain
GROUP BY "Delivery Status"
ORDER BY record_count DESC;


-- ============================================================
-- 8. ORDER STATUS ANALYSIS
-- ============================================================

SELECT
    "Order Status",
    COUNT(DISTINCT "Order Id") AS unique_orders
FROM supply_chain
GROUP BY "Order Status"
ORDER BY unique_orders DESC;


-- ============================================================
-- 9. TOTAL SALES
-- ============================================================

SELECT
    SUM(Sales) AS total_sales
FROM supply_chain;


-- ============================================================
-- 10. TOTAL PROFIT
-- ============================================================

SELECT
    SUM("Order Profit Per Order") AS total_profit
FROM supply_chain;


-- ============================================================
-- 11. SALES BY CATEGORY
-- ============================================================

SELECT
    "Category Name",
    SUM(Sales) AS total_sales
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_sales DESC;


-- ============================================================
-- 12. PROFIT BY CATEGORY
-- ============================================================

SELECT
    "Category Name",
    SUM("Order Profit Per Order") AS total_profit
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_profit DESC;


-- ============================================================
-- 13. SALES BY REGION
-- ============================================================

SELECT
    "Order Region",
    SUM(Sales) AS total_sales
FROM supply_chain
GROUP BY "Order Region"
ORDER BY total_sales DESC;


-- ============================================================
-- 14. LATE DELIVERY % BY SHIPPING MODE
-- ============================================================

SELECT
    "Shipping Mode",
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN "Late_delivery_risk" = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
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
ORDER BY late_delivery_percentage DESC;


-- ============================================================
-- 15. LATE DELIVERY % BY REGION
-- ============================================================

SELECT
    "Order Region",
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN "Late_delivery_risk" = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
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
GROUP BY "Order Region"
ORDER BY late_delivery_percentage DESC;


-- ============================================================
-- 16. LATE DELIVERY % BY MARKET
-- ============================================================

SELECT
    Market,
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN "Late_delivery_risk" = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
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
GROUP BY Market
ORDER BY late_delivery_percentage DESC;


-- ============================================================
-- 17. TOTAL UNITS SOLD
-- ============================================================

SELECT
    SUM("Order Item Quantity") AS total_units_sold
FROM supply_chain;


-- ============================================================
-- 18. AVERAGE ORDER VALUE
-- ============================================================

SELECT
    ROUND(
        SUM(Sales) / COUNT(DISTINCT "Order Id"),
        2
    ) AS average_order_value
FROM supply_chain;


-- ============================================================
-- 19. AVERAGE SHIPPING COST
-- ============================================================

SELECT
    ROUND(AVG("Shipping cost"), 2) AS average_shipping_cost
FROM supply_chain;


-- ============================================================
-- 20. AVERAGE DELIVERY / SHIPPING DURATION
-- ============================================================

SELECT
    ROUND(
        AVG(
            julianday("shipping date (DateOrders)")
            - julianday("order date (DateOrders)")
        ),
        2
    ) AS average_shipping_duration_days
FROM supply_chain
WHERE "shipping date (DateOrders)" IS NOT NULL
  AND "order date (DateOrders)" IS NOT NULL;


-- ============================================================
-- 21. ON-TIME DELIVERY RATE
-- ============================================================

SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN "Late_delivery_risk" = 0 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS on_time_delivery_rate
FROM supply_chain;


-- ============================================================
-- 22. LATE DELIVERY RATE
-- ============================================================

SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN "Late_delivery_risk" = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_delivery_rate
FROM supply_chain;


-- ============================================================
-- 23. SALES BY CUSTOMER SEGMENT
-- ============================================================

SELECT
    "Customer Segment",
    SUM(Sales) AS total_sales,
    COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain
GROUP BY "Customer Segment"
ORDER BY total_sales DESC;


-- ============================================================
-- 24. TOP 10 PRODUCTS BY SALES
-- ============================================================

SELECT
    "Product Name",
    SUM(Sales) AS total_sales,
    SUM("Order Item Quantity") AS units_sold
FROM supply_chain
GROUP BY "Product Name"
ORDER BY total_sales DESC
LIMIT 10;


-- ============================================================
-- 25. TOP 10 REGIONS BY SALES
-- ============================================================

SELECT
    "Order Region",
    SUM(Sales) AS total_sales,
    COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain
GROUP BY "Order Region"
ORDER BY total_sales DESC
LIMIT 10;


-- ============================================================
-- 26. MONTHLY SALES
-- ============================================================

SELECT
    strftime(
        '%Y-%m',
        "order date (DateOrders)"
    ) AS month,
    ROUND(SUM(Sales), 2) AS monthly_sales
FROM supply_chain
WHERE "order date (DateOrders)" IS NOT NULL
GROUP BY month
ORDER BY month;


-- ============================================================
-- 27. MONTH-OVER-MONTH SALES GROWTH
-- ============================================================

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
    ROUND(previous_month_sales, 2) AS previous_month_sales,
    ROUND(
        100.0 * (sales - previous_month_sales)
        / NULLIF(previous_month_sales, 0),
        2
    ) AS mom_growth_percentage
FROM sales_with_previous
ORDER BY month;


-- ============================================================
-- 28. REGIONAL SALES RANKING
-- ============================================================

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
ORDER BY sales_rank;


-- ============================================================
-- 29. SHIPPING MODE PERFORMANCE
-- ============================================================

SELECT
    "Shipping Mode",
    COUNT(DISTINCT "Order Id") AS total_orders,
    ROUND(AVG("Shipping cost"), 2) AS avg_shipping_cost,
    ROUND(
        AVG(
            "Days for shipment (actual)"
        ),
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
ORDER BY late_delivery_percentage DESC;


-- ============================================================
-- 30. HIGH-SALES PRODUCTS WITH DELIVERY ISSUES
-- ============================================================

SELECT
    "Product Name",
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN "Late_delivery_risk" = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
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
ORDER BY total_sales DESC, late_delivery_percentage DESC;


-- ============================================================
-- 31. MONTHLY REGIONAL SALES RANKING
-- ============================================================

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
ORDER BY month, regional_rank;


-- ============================================================
-- 32. FAST-MOVING PRODUCTS
-- ============================================================

SELECT
    "Product Name",
    SUM("Order Item Quantity") AS units_sold,
    SUM(Sales) AS total_sales
FROM supply_chain
GROUP BY "Product Name"
ORDER BY units_sold DESC
LIMIT 10;


-- ============================================================
-- 33. SLOW-MOVING PRODUCTS
-- ============================================================

SELECT
    "Product Name",
    SUM("Order Item Quantity") AS units_sold,
    SUM(Sales) AS total_sales
FROM supply_chain
GROUP BY "Product Name"
ORDER BY units_sold ASC
LIMIT 10;


-- ============================================================
-- 34. DEMAND BY MONTH
-- ============================================================

SELECT
    strftime(
        '%Y-%m',
        "order date (DateOrders)"
    ) AS month,
    SUM("Order Item Quantity") AS monthly_units
FROM supply_chain
WHERE "order date (DateOrders)" IS NOT NULL
GROUP BY month
ORDER BY month;


-- ============================================================
-- 35. DEMAND BY PRODUCT CATEGORY
-- ============================================================

SELECT
    "Category Name",
    SUM("Order Item Quantity") AS total_units,
    ROUND(AVG("Order Item Quantity"), 2) AS avg_quantity_per_record
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_units DESC;


-- ============================================================
-- 36. DEMAND VARIABILITY BY PRODUCT
-- ============================================================

SELECT
    "Product Name",
    COUNT(*) AS observations,
    ROUND(AVG("Order Item Quantity"), 2) AS avg_quantity,
    ROUND(
        (
            AVG("Order Item Quantity" * "Order Item Quantity")
            - AVG("Order Item Quantity")
              * AVG("Order Item Quantity")
        ),
        2
    ) AS quantity_variance
FROM supply_chain
GROUP BY "Product Name"
ORDER BY quantity_variance DESC;


-- ============================================================
-- 37. OVERALL DESCRIPTIVE STATISTICS
-- ============================================================

SELECT
    COUNT(Sales) AS sales_count,
    ROUND(AVG(Sales), 2) AS avg_sales,
    ROUND(MIN(Sales), 2) AS min_sales,
    ROUND(MAX(Sales), 2) AS max_sales,
    ROUND(AVG("Order Item Quantity"), 2) AS avg_quantity,
    ROUND(MIN("Order Item Quantity"), 2) AS min_quantity,
    ROUND(MAX("Order Item Quantity"), 2) AS max_quantity,
    ROUND(AVG("Shipping cost"), 2) AS avg_shipping_cost,
    ROUND(MIN("Shipping cost"), 2) AS min_shipping_cost,
    ROUND(MAX("Shipping cost"), 2) AS max_shipping_cost
FROM supply_chain;


-- ============================================================
-- 38. DELIVERY TIME STATISTICS BY SHIPPING MODE
-- ============================================================

SELECT
    "Shipping Mode",
    COUNT(*) AS records,
    ROUND(
        AVG("Days for shipment (actual)"),
        2
    ) AS avg_delivery_days,
    MIN("Days for shipment (actual)")
        AS minimum_delivery_days,
    MAX("Days for shipment (actual)")
        AS maximum_delivery_days
FROM supply_chain
GROUP BY "Shipping Mode"
ORDER BY avg_delivery_days DESC;


-- ============================================================
-- 39. CORRELATION INPUTS FOR SALES AND SHIPPING COST
-- ============================================================

SELECT
    COUNT(*) AS observations,
    ROUND(AVG(Sales), 2) AS avg_sales,
    ROUND(AVG("Shipping cost"), 2) AS avg_shipping_cost,
    ROUND(AVG("Order Item Quantity"), 2) AS avg_quantity
FROM supply_chain;


-- ============================================================
-- 40. DELIVERY PERFORMANCE BY CUSTOMER SEGMENT
-- ============================================================

SELECT
    "Customer Segment",
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN "Late_delivery_risk" = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
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
GROUP BY "Customer Segment"
ORDER BY late_delivery_percentage DESC;


-- ============================================================
-- 41. SALES AND DELIVERY ISSUES BY CATEGORY
-- ============================================================

SELECT
    "Category Name",
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN "Late_delivery_risk" = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
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
GROUP BY "Category Name"
ORDER BY total_sales DESC;


-- ============================================================
-- 42. CUMULATIVE SALES BY MONTH
-- ============================================================

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
ORDER BY month;


-- ============================================================
-- 43. TOP PRODUCTS WITH LATE DELIVERY
-- ============================================================

SELECT
    "Product Name",
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN "Late_delivery_risk" = 1 THEN 1
            ELSE 0
        END
    ) AS late_records,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN "Late_delivery_risk" = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_percentage,
    ROUND(SUM(Sales), 2) AS total_sales
FROM supply_chain
GROUP BY "Product Name"
HAVING late_records > 0
ORDER BY late_percentage DESC
LIMIT 10;


-- ============================================================
-- 44. SALES BY YEAR
-- ============================================================

SELECT
    strftime(
        '%Y',
        "order date (DateOrders)"
    ) AS year,
    ROUND(SUM(Sales), 2) AS total_sales
FROM supply_chain
WHERE "order date (DateOrders)" IS NOT NULL
GROUP BY year
ORDER BY year;


-- ============================================================
-- 45. ORDERS BY YEAR
-- ============================================================

SELECT
    strftime(
        '%Y',
        "order date (DateOrders)"
    ) AS year,
    COUNT(DISTINCT "Order Id") AS total_orders
FROM supply_chain
WHERE "order date (DateOrders)" IS NOT NULL
GROUP BY year
ORDER BY year;


-- ============================================================
-- END OF SQL ANALYSIS
-- ============================================================