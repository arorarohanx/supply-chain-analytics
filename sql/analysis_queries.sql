-- =========================================================
-- PHASE 4: SUPPLY CHAIN SQL ANALYSIS
-- Database table: supply_chain
-- =========================================================


-- QUERY 1: Overall business overview

SELECT
    COUNT(*) AS total_order_items,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(DISTINCT order_item_id) AS unique_order_items,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(order_item_total), 2) AS total_order_item_value
FROM supply_chain;


-- QUERY 2: Distribution of delivery statuses

SELECT
    delivery_status,
    COUNT(*) AS total_records,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM supply_chain),
        2
    ) AS percentage
FROM supply_chain
GROUP BY delivery_status
ORDER BY total_records DESC;


-- QUERY 3: Overall late delivery performance
-- Canceled records are excluded from the late-rate denominator.

SELECT
    COUNT(*) AS non_cancelled_records,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_records,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
WHERE delivery_status != 'Shipping canceled';


-- QUERY 4: Delivery performance by shipping mode

SELECT
    shipping_mode,
    COUNT(*) AS non_cancelled_records,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_records,
    SUM(CASE
        WHEN delivery_status = 'Shipping on time' THEN 1
        ELSE 0
    END) AS on_time_records,
    SUM(CASE
        WHEN delivery_status = 'Advance shipping' THEN 1
        ELSE 0
    END) AS advance_records,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
WHERE delivery_status != 'Shipping canceled'
GROUP BY shipping_mode
ORDER BY late_delivery_percentage DESC;


-- QUERY 5: Delivery performance by region

SELECT
    order_region,
    COUNT(*) AS non_cancelled_records,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_records,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
WHERE delivery_status != 'Shipping canceled'
GROUP BY order_region
ORDER BY late_delivery_percentage DESC;


-- QUERY 6: Delivery performance by product category

SELECT
    category_name,
    COUNT(*) AS total_records,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_records,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
WHERE delivery_status != 'Shipping canceled'
GROUP BY category_name
ORDER BY late_delivery_percentage DESC;


-- QUERY 7: Monthly order-item volume

SELECT
    strftime('%Y-%m', order_date_dateorders) AS order_month,
    COUNT(*) AS total_order_items,
    COUNT(DISTINCT order_id) AS unique_orders
FROM supply_chain
GROUP BY order_month
ORDER BY order_month;


-- QUERY 8: Relationship between order status and delivery status

SELECT
    order_status,
    delivery_status,
    COUNT(*) AS total_records
FROM supply_chain
GROUP BY order_status, delivery_status
ORDER BY total_records DESC;


-- QUERY 9: Shipping delay by shipping mode

SELECT
    shipping_mode,
    COUNT(*) AS total_records,
    ROUND(AVG(days_for_shipping_real), 2) AS avg_actual_shipping_days,
    ROUND(AVG(days_for_shipment_scheduled), 2) AS avg_scheduled_shipping_days,
    ROUND(AVG(shipping_delay_days), 2) AS avg_shipping_delay_days
FROM supply_chain
WHERE delivery_status != 'Shipping canceled'
GROUP BY shipping_mode
ORDER BY avg_shipping_delay_days DESC;


-- QUERY 10: Financial performance by product category

SELECT
    category_name,
    COUNT(*) AS total_order_items,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(order_item_total), 2) AS total_order_item_value,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit
FROM supply_chain
GROUP BY category_name
ORDER BY total_sales DESC;


-- QUERY 11: Financial performance by region

SELECT
    order_region,
    COUNT(*) AS total_order_items,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit
FROM supply_chain
GROUP BY order_region
ORDER BY total_sales DESC;


-- QUERY 12: Financial exposure associated with late deliveries
-- These values represent sales/value associated with late items,
-- NOT proven financial losses caused by delays.

SELECT
    COUNT(*) AS late_order_items,
    ROUND(SUM(sales), 2) AS sales_associated_with_late_items,
    ROUND(SUM(order_item_total), 2) AS item_value_associated_with_late_items,
    ROUND(AVG(shipping_delay_days), 2) AS avg_delay_days
FROM supply_chain
WHERE delivery_status = 'Late delivery';


-- QUERY 13: Delivery performance by region and shipping mode

SELECT
    order_region,
    shipping_mode,
    COUNT(*) AS non_cancelled_records,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_records,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
WHERE delivery_status != 'Shipping canceled'
GROUP BY order_region, shipping_mode
HAVING COUNT(*) >= 100
ORDER BY late_delivery_percentage DESC;


-- QUERY 14: Delivery performance by market

SELECT
    market,
    COUNT(*) AS non_cancelled_records,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_records,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
WHERE delivery_status != 'Shipping canceled'
GROUP BY market
ORDER BY late_delivery_percentage DESC;


-- QUERY 15: Monthly late delivery trend

SELECT
    strftime('%Y-%m', order_date_dateorders) AS order_month,
    COUNT(*) AS non_cancelled_records,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_records,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain
WHERE delivery_status != 'Shipping canceled'
GROUP BY order_month
ORDER BY order_month;