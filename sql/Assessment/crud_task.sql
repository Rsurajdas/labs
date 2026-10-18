CREATE TABLE products (
    -- id SERIAL PRIMARY KEY,
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(8, 2),
    stock INT,
    created_at DATE DEFAULT (CURRENT_DATE)
);
INSERT INTO products (product_name, category, price, stock, created_at)
VALUES (
        'Laptop',
        'Electronics',
        75000.00,
        12,
        '2024-01-15'
    ),
    (
        'Mouse',
        'Electronics',
        550.00,
        200,
        '2024-02-10'
    ),
    (
        'Notebook',
        'Stationery',
        45.00,
        500,
        '2024-01-20'
    ),
    (
        'Desk Chair',
        'Furniture',
        8500.00,
        30,
        '2024-03-05'
    ),
    (
        'Monitor',
        'Electronics',
        15000.00,
        45,
        '2024-02-28'
    ),
    (
        'Pen',
        'Stationery',
        10.00,
        1000,
        '2024-03-12'
    ),
    (
        'Standing Desk',
        'Furniture',
        22000.00,
        8,
        '2024-01-30'
    );
SELECT *
FROM products;
SELECT product_name,
    price
FROM products;
SELECT *
FROM products
WHERE category = 'Electronics';
SELECT *
FROM products
WHERE price > 10000;
SELECT *
FROM products
ORDER BY price DESC;
SELECT product_name,
    stock
FROM products
ORDER BY stock
LIMIT 3;
SELECT *
FROM products
ORDER BY created_at ASC
LIMIT 3 OFFSET 2;
UPDATE products
SET price = 12.00
WHERE id = 6;
DELETE FROM products
WHERE stock < 10;
SELECT product_name,
    price
FROM products
WHERE category = 'Furniture'
ORDER BY price DESC
LIMIT 1;