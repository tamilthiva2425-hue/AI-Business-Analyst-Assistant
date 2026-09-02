USE business_analytics;

-- 1. Monthly Revenue
SELECT
    DATE_FORMAT(sale_date, '%Y-%m') AS sales_month,
    SUM(total_amount) AS total_revenue,
    COUNT(sale_id) AS total_transactions,
    SUM(quantity) AS units_sold
FROM sales
GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
ORDER BY sales_month;


-- 2. Revenue by Region
SELECT
    region,
    SUM(total_amount) AS total_revenue,
    COUNT(sale_id) AS total_transactions,
    SUM(quantity) AS units_sold
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;


-- 3. Payment Method Performance
SELECT
    payment_method,
    COUNT(sale_id) AS transactions,
    SUM(total_amount) AS total_revenue
FROM sales
GROUP BY payment_method
ORDER BY total_revenue DESC;


-- 4. Top 10 Products by Revenue
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(s.quantity) AS units_sold,
    SUM(s.total_amount) AS total_revenue
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_revenue DESC
LIMIT 10;


-- 5. Customer Segment Performance
SELECT
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(s.sale_id) AS transactions,
    SUM(s.total_amount) AS total_revenue
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;