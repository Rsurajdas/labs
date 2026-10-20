CREATE TABLE sales(
    id INT PRIMARY KEY AUTO_INCREMENT,
    -- id SERIAL PRIMARY KEY,
    date_created DATE DEFAULT (CURRENT_DATE),
    date_fulfiled DATE,
    customer_name VARCHAR(100) NOT NULL,
    product_name VARCHAR(300) NOT NULL,
    price NUMERIC(10, 2) CHECK (price > 0),
    is_recurring BOOLEAN DEFAULT FALSE,
    is_disputed BOOLEAN DEFAULT FALSE
);
UPDATE sales
SET date_fulfiled = NULL
WHERE is_disputed = TRUE;
SELECT *
FROM sales
WHERE price > 6999;
SELECT *
FROM sales
WHERE is_recurring IS TRUE;
SELECT *
FROM sales
WHERE (is_disputed IS TRUE)
    AND (price > 5000);
SELECT *
FROM sales
WHERE date_created > '2026-02-15'
    AND date_created < '2026-03-17';
SELECT *
FROM sales
WHERE date_created BETWEEN '2026-02-15' AND '2026-03-17';
SELECT *
FROM sales
WHERE customer_name = 'Amit Thakur';
SELECT *
FROM sales
WHERE customer_name <> 'Amit Thakur';
SELECT *
FROM sales
WHERE date_fulfiled - date_created <= 2;
SELECT *
FROM sales
ORDER BY price DESC
LIMIT 10;
SELECT *
FROM sales
ORDER BY price
LIMIT 10;
SELECT *
FROM sales
WHERE is_disputed IS FALSE
ORDER BY price
LIMIT 10;
SELECT DISTINCT customer_name
FROM sales
ORDER BY customer_name;
Subqueries CREATE VIEW base_result AS
SELECT *
FROM sales
WHERE price > 2999;
SELECT customer_name,
    product_name
FROM base_result;