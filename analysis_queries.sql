-- ============================================================
-- RetailIQ — SQL Analysis Queries
-- Dataset: Online Retail II (UCI)
-- Author: Sri Sai Samarth Sistla
-- ============================================================


-- ── 1. Monthly Revenue Trend ──────────────────────────────
SELECT 
    strftime('%Y-%m', invoice_date) AS month,
    ROUND(SUM(revenue), 2)          AS total_revenue,
    COUNT(DISTINCT invoice_id)      AS total_orders,
    COUNT(DISTINCT customer_id)     AS unique_customers
FROM retail
GROUP BY month
ORDER BY month;


-- ── 2. Top 10 Products by Revenue ────────────────────────
SELECT 
    product_name,
    SUM(quantity)          AS total_units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM retail
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- ── 3. Revenue by Country ─────────────────────────────────
SELECT 
    country,
    ROUND(SUM(revenue), 2)      AS total_revenue,
    COUNT(DISTINCT customer_id)  AS customers,
    COUNT(DISTINCT invoice_id)   AS total_orders
FROM retail
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 10;


-- ── 4. Average Order Value by Country ────────────────────
SELECT 
    country,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    COUNT(DISTINCT invoice_id) AS total_orders
FROM retail
GROUP BY country
ORDER BY avg_order_value DESC
LIMIT 10;


-- ── 5. Best Selling Day of Week ───────────────────────────
SELECT 
    day_of_week,
    ROUND(SUM(revenue), 2)     AS total_revenue,
    COUNT(DISTINCT invoice_id)  AS total_orders
FROM retail
GROUP BY day_of_week
ORDER BY total_revenue DESC;


-- ── 6. Customer Lifetime Value ────────────────────────────
SELECT 
    customer_id,
    COUNT(DISTINCT invoice_id)  AS total_orders,
    ROUND(SUM(revenue), 2)      AS lifetime_value,
    ROUND(AVG(revenue), 2)      AS avg_order_value,
    MIN(invoice_date)           AS first_purchase,
    MAX(invoice_date)           AS last_purchase
FROM retail
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 20;


-- ── 7. Revenue by Hour of Day ─────────────────────────────
SELECT 
    hour,
    ROUND(SUM(revenue), 2)     AS total_revenue,
    COUNT(DISTINCT invoice_id)  AS total_orders
FROM retail
GROUP BY hour
ORDER BY hour;


-- ── 8. Monthly New vs Returning Customers ─────────────────
SELECT 
    strftime('%Y-%m', invoice_date) AS month,
    COUNT(DISTINCT customer_id)     AS active_customers,
    ROUND(SUM(revenue), 2)          AS total_revenue,
    ROUND(SUM(revenue) / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM retail
GROUP BY month
ORDER BY month;
