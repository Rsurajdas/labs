CREATE DATABASE shop;
CREATE TABLE products(
    product_name VARCHAR(400),
    price FLOAT,
    description TEXT,
    stock INT,
    image VARCHAR(300)
);
INSERT INTO products
VALUES (
        'Wireless Mouse',
        799.00,
        'Ergonomic wireless mouse with USB receiver',
        50,
        'wireless-mouse.jpg'
    ),
    (
        'Mechanical Keyboard',
        2499.00,
        'RGB mechanical keyboard with blue switches',
        30,
        'mechanical-keyboard.jpg'
    ),
    (
        'USB-C Hub',
        1499.00,
        'Multi-port USB-C hub with HDMI and USB 3.0',
        25,
        'usb-c-hub.jpg'
    ),
    (
        'Laptop Stand',
        1299.00,
        'Adjustable aluminum stand for laptops',
        40,
        'laptop-stand.jpg'
    ),
    (
        'Bluetooth Speaker',
        1999.00,
        'Portable Bluetooth speaker with powerful bass',
        20,
        'bluetooth-speaker.jpg'
    ),
    (
        'Webcam',
        1799.00,
        'Full HD 1080p webcam with built-in microphone',
        35,
        'webcam.jpg'
    ),
    (
        'Gaming Headset',
        2999.00,
        'Over-ear gaming headset with surround sound',
        15,
        'gaming-headset.jpg'
    ),
    (
        'Power Bank',
        1599.00,
        '10000mAh portable power bank with fast charging',
        45,
        'power-bank.jpg'
    ),
    (
        'Smart Watch',
        3499.00,
        'Fitness smart watch with heart rate monitoring',
        18,
        'smart-watch.jpg'
    ),
    (
        'Portable SSD',
        4999.00,
        '500GB portable SSD with high-speed data transfer',
        12,
        'portable-ssd.jpg'
    );
-- MySQL
ALTER TABLE products
MODIFY COLUMN product_name VARCHAR(400) NOT NULL,
    ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT;
-- PostgreSQL
ALTER TABLE products
ALTER COLUMN product_name
SET NOT NULL,
    ADD COLUMN id SERIAL PRIMARY KEY;
-- MySQL
ALTER TABLE products
ADD CONSTRAINT check_price CHECK (price > 0),
    ADD CONSTRAINT check_stock CHECK (stock >= 0),
    MODIFY COLUMN description TEXT NOT NULL;
-- PostgreSQL
ALTER TABLE products
ADD CONSTRAINT check_price CHECK(price > 0),
    ADD CONSTRAINT check_stock CHECK(stock >= 0),
    ALTER COLUMN description
SET NOT NULL;