
SELECT * FROM olist_orders LIMIT 10;

SELECT to_char(order_purchase_timestamp, 'YYYY-MM') AS month, COUNT(*) AS orders
FROM olist_orders
GROUP BY month
ORDER BY month;

SELECT oi.order_id, SUM(oi.price) AS order_total
FROM olist_order_items oi
GROUP BY oi.order_id;

SELECT p.product_id, AVG(r.review_score) as avg_score, COUNT(r.review_id) as reviews_count
FROM olist_order_items oi
JOIN olist_order_reviews r ON oi.order_id = r.order_id
JOIN olist_products p ON oi.product_id = p.product_id
GROUP BY p.product_id
ORDER BY avg_score DESC NULLS LAST
LIMIT 20;

SELECT c.customer_state, SUM(oi.price) as total_sales, COUNT(DISTINCT o.order_id) as orders
FROM olist_customers c
JOIN olist_orders o ON c.customer_id = o.customer_id
JOIN olist_order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY total_sales DESC;

SELECT pt.product_category_name_english, SUM(oi.price) as total_sales
FROM olist_order_items oi
JOIN olist_products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation pt ON p.product_category_name = pt.product_category_name
GROUP BY pt.product_category_name_english
ORDER BY total_sales DESC;

SELECT AVG((order_delivered_customer_date - order_purchase_timestamp)) AS avg_days,
       MIN((order_delivered_customer_date - order_purchase_timestamp)) AS min_days,
       MAX((order_delivered_customer_date - order_purchase_timestamp)) AS max_days
FROM olist_orders
WHERE order_delivered_customer_date IS NOT NULL AND order_purchase_timestamp IS NOT NULL;

SELECT payment_type, SUM(payment_value) as total, AVG(payment_value) as avg
FROM olist_order_payments
GROUP BY payment_type
ORDER BY total DESC;

SELECT s.seller_id, s.seller_state, SUM(oi.price) as total_sales, COUNT(DISTINCT oi.order_id) as orders
FROM olist_sellers s
JOIN olist_order_items oi ON s.seller_id = oi.seller_id
GROUP BY s.seller_id, s.seller_state
ORDER BY total_sales DESC
LIMIT 20;

SELECT order_id, COUNT(*) as cnt
FROM olist_order_items
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY cnt DESC;
