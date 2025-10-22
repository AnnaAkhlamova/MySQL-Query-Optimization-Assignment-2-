CREATE DATABASE hw2;
USE hw2;
SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM orders;
SHOW INDEXES FROM customers;
SHOW INDEXES FROM products;
SHOW INDEXES FROM orders;
-- НЕ-ОПТИМІЗОВАНИЙ ЗАПИТ (AI-generated)
SELECT DISTINCT
  c.id,
  c.name,
  c.email,
  c.country,
  c.city,
  COUNT(o.id) AS total_orders,
  SUM(o.quantity) AS total_quantity,
  SUM(p.price * o.quantity) AS total_spent,
  MAX(o.order_date) AS last_order_date
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN products p ON p.id = o.product_id
WHERE (c.country = 'United States' OR c.country LIKE '%United%')
  AND DATE(o.order_date) >= '2024-01-01'
GROUP BY c.id
HAVING total_orders > 5
ORDER BY total_spent DESC
LIMIT 100;

CREATE INDEX idx_customers_country_id
ON customers (country, id);
DROP INDEX idx_customers_country_id ON customers;
DROP INDEX idx_orders_date_customer_product ON orders;
CREATE INDEX idx_orders_date_customer_product
ON orders (order_date, customer_id, product_id);

WITH recent_orders AS (
    SELECT id, order_date, customer_id, product_id, quantity
    FROM orders USE INDEX (idx_orders_date_customer_product)
    WHERE order_date >= '2024-01-01'
)
SELECT
    c.id,
    c.name,
    c.email,
    c.country,
    c.city,
    COUNT(o.id) AS total_orders,
    SUM(o.quantity) AS total_quantity,
    SUM(p.price * o.quantity) AS total_spent,
    MAX(o.order_date) AS last_order_date
FROM customers c USE INDEX (idx_customers_country_id)
JOIN recent_orders o
    ON c.id = o.customer_id
JOIN products p
    ON p.id = o.product_id
WHERE c.country LIKE 'United%'
GROUP BY c.id, c.name, c.email, c.country, c.city
HAVING total_orders > 5
ORDER BY total_spent DESC
LIMIT 100;

EXPLAIN SELECT DISTINCT
  c.id,
  c.name,
  c.email,
  c.country,
  c.city,
  COUNT(o.id) AS total_orders,
  SUM(o.quantity) AS total_quantity,
  SUM(p.price * o.quantity) AS total_spent,
  MAX(o.order_date) AS last_order_date
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN products p ON p.id = o.product_id
WHERE (c.country = 'United States' OR c.country LIKE '%United%')
  AND DATE(o.order_date) >= '2024-01-01'
GROUP BY c.id
HAVING total_orders > 5
ORDER BY total_spent DESC
LIMIT 100;

EXPLAIN WITH recent_orders AS (
    SELECT id, customer_id, quantity, product_id, order_date
    FROM orders
    WHERE order_date >= '2024-01-01'
)
SELECT
    c.id,
    c.name,
    c.email,
    c.country,
    c.city,
    COUNT(o.id) AS total_orders,
    SUM(o.quantity) AS total_quantity,
    SUM(p.price * o.quantity) AS total_spent,
    MAX(o.order_date) AS last_order_date
FROM customers c USE INDEX (idx_customers_country_id)
JOIN recent_orders o
    ON c.id = o.customer_id
JOIN products p
    ON p.id = o.product_id
WHERE c.country LIKE 'United%'
GROUP BY c.id, c.name, c.email, c.country, c.city
HAVING total_orders > 5
ORDER BY total_spent DESC
LIMIT 100;
