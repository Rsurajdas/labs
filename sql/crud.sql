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
INSERT INTO sales (
        date_created,
        date_fulfiled,
        customer_name,
        product_name,
        price,
        is_recurring,
        is_disputed
    )
VALUES (
        '2026-01-03',
        '2026-01-05',
        'Aarav Sharma',
        'Wireless Keyboard',
        2499.00,
        FALSE,
        FALSE
    ),
    (
        '2026-01-04',
        '2026-01-07',
        'Priya Verma',
        'Bluetooth Headphones',
        3499.00,
        TRUE,
        FALSE
    ),
    (
        '2026-01-06',
        '2026-01-09',
        'Rahul Mehta',
        'Mechanical Keyboard',
        5999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-01-08',
        '2026-01-11',
        'Sneha Iyer',
        'USB-C Docking Station',
        4299.00,
        TRUE,
        FALSE
    ),
    (
        '2026-01-10',
        '2026-01-13',
        'Vikram Singh',
        '27-inch LED Monitor',
        15999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-01-12',
        '2026-01-15',
        'Ananya Kapoor',
        'Wireless Mouse',
        1799.00,
        FALSE,
        FALSE
    ),
    (
        '2026-01-14',
        '2026-01-17',
        'Rohan Gupta',
        'Laptop Stand',
        2299.00,
        TRUE,
        FALSE
    ),
    (
        '2026-01-16',
        '2026-01-19',
        'Neha Nair',
        'External SSD 1TB',
        7499.00,
        FALSE,
        TRUE
    ),
    (
        '2026-01-18',
        '2026-01-21',
        'Karan Malhotra',
        'Webcam Full HD',
        3299.00,
        FALSE,
        FALSE
    ),
    (
        '2026-01-20',
        '2026-01-23',
        'Meera Joshi',
        'Noise Cancelling Earbuds',
        4999.00,
        TRUE,
        FALSE
    ),
    (
        '2026-01-22',
        '2026-01-25',
        'Aditya Rao',
        'Ergonomic Office Chair',
        18999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-01-24',
        '2026-01-27',
        'Pooja Shah',
        'Portable Power Bank',
        1999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-01-26',
        '2026-01-29',
        'Arjun Patel',
        'Smartphone Tripod',
        1499.00,
        TRUE,
        FALSE
    ),
    (
        '2026-01-28',
        '2026-01-31',
        'Kavya Reddy',
        '24-inch LED Monitor',
        11999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-01-30',
        '2026-02-02',
        'Siddharth Das',
        'Wi-Fi 6 Router',
        5499.00,
        FALSE,
        TRUE
    ),
    (
        '2026-02-01',
        '2026-02-04',
        'Ishita Bose',
        'USB-C Hub',
        1899.00,
        TRUE,
        FALSE
    ),
    (
        '2026-02-03',
        '2026-02-06',
        'Nikhil Sinha',
        'Gaming Mouse',
        2799.00,
        FALSE,
        FALSE
    ),
    (
        '2026-02-05',
        '2026-02-08',
        'Divya Menon',
        'Gaming Headset',
        4499.00,
        FALSE,
        FALSE
    ),
    (
        '2026-02-07',
        '2026-02-10',
        'Manish Kumar',
        'Laptop Backpack',
        2999.00,
        TRUE,
        FALSE
    ),
    (
        '2026-02-09',
        '2026-02-12',
        'Simran Kaur',
        'Portable Bluetooth Speaker',
        3799.00,
        FALSE,
        FALSE
    ),
    (
        '2026-02-11',
        '2026-02-14',
        'Yash Agarwal',
        'Smart LED Bulb Pack',
        1599.00,
        TRUE,
        FALSE
    ),
    (
        '2026-02-13',
        '2026-02-16',
        'Tanvi Kulkarni',
        'Smart Watch',
        6999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-02-15',
        '2026-02-18',
        'Harsh Vardhan',
        'Fitness Tracker',
        3299.00,
        FALSE,
        TRUE
    ),
    (
        '2026-02-17',
        '2026-02-20',
        'Ritika Bansal',
        'Tablet Stand',
        1299.00,
        TRUE,
        FALSE
    ),
    (
        '2026-02-19',
        '2026-02-22',
        'Abhishek Jain',
        '1080p Projector',
        12999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-02-21',
        '2026-02-24',
        'Nandini Rao',
        'Wireless Charger',
        2199.00,
        TRUE,
        FALSE
    ),
    (
        '2026-02-23',
        '2026-02-26',
        'Saurabh Mishra',
        'Smartphone Gimbal',
        8999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-02-25',
        '2026-02-28',
        'Aditi Chawla',
        'Noise Cancelling Headphones',
        8499.00,
        FALSE,
        FALSE
    ),
    (
        '2026-02-27',
        '2026-03-02',
        'Varun Khanna',
        'External Hard Drive 2TB',
        6499.00,
        TRUE,
        TRUE
    ),
    (
        '2026-03-01',
        '2026-03-04',
        'Shreya Pandey',
        'USB Microphone',
        3999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-03-03',
        '2026-03-06',
        'Mohit Bhatia',
        'Streaming Webcam',
        5299.00,
        FALSE,
        FALSE
    ),
    (
        '2026-03-05',
        '2026-03-08',
        'Isha Srivastava',
        'Desk Lamp',
        2499.00,
        TRUE,
        FALSE
    ),
    (
        '2026-03-07',
        '2026-03-10',
        'Deepak Yadav',
        'Smart Plug 4-Pack',
        2899.00,
        FALSE,
        FALSE
    ),
    (
        '2026-03-09',
        '2026-03-12',
        'Swati Tiwari',
        'Portable Monitor',
        13999.00,
        FALSE,
        TRUE
    ),
    (
        '2026-03-11',
        '2026-03-14',
        'Akash Saxena',
        'Laptop Cooling Pad',
        1999.00,
        TRUE,
        FALSE
    ),
    (
        '2026-03-13',
        '2026-03-16',
        'Komal Gupta',
        'Mechanical Gaming Keyboard',
        6999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-03-15',
        '2026-03-18',
        'Rajiv Chopra',
        '4K LED Monitor',
        24999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-03-17',
        '2026-03-20',
        'Preeti Soni',
        'Wireless Presenter',
        1799.00,
        TRUE,
        FALSE
    ),
    (
        '2026-03-19',
        '2026-03-22',
        'Amit Thakur',
        'NAS Storage 4TB',
        22999.00,
        FALSE,
        TRUE
    ),
    (
        '2026-03-21',
        '2026-03-24',
        'Shalini Arora',
        'Smart Home Security Camera',
        4599.00,
        TRUE,
        FALSE
    ),
    (
        '2026-03-23',
        '2026-03-26',
        'Gaurav Bansal',
        'USB-C Fast Charger',
        2499.00,
        FALSE,
        FALSE
    ),
    (
        '2026-03-25',
        '2026-03-28',
        'Madhuri Rao',
        'Tablet 10-inch',
        17999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-03-27',
        '2026-03-30',
        'Rakesh Pillai',
        'Wi-Fi Range Extender',
        3299.00,
        TRUE,
        FALSE
    ),
    (
        '2026-03-29',
        '2026-04-01',
        'Nisha Agarwal',
        'Smart Door Lock',
        8999.00,
        FALSE,
        TRUE
    ),
    (
        '2026-03-31',
        '2026-04-03',
        'Sanjay Menon',
        'Office Desk',
        12999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-04-02',
        '2026-04-05',
        'Pallavi Deshmukh',
        'All-in-One Printer',
        11499.00,
        TRUE,
        FALSE
    ),
    (
        '2026-04-04',
        '2026-04-07',
        'Ravi Shukla',
        'Laser Printer',
        15499.00,
        FALSE,
        FALSE
    ),
    (
        '2026-04-06',
        '2026-04-09',
        'Juhi Saxena',
        'Document Scanner',
        7999.00,
        FALSE,
        FALSE
    ),
    (
        '2026-04-08',
        '2026-04-11',
        'Naveen Reddy',
        'Conference Speakerphone',
        9499.00,
        TRUE,
        TRUE
    ),
    (
        '2026-04-10',
        '2026-04-13',
        'Alisha Roy',
        'Smart TV 43-inch',
        28999.00,
        FALSE,
        FALSE
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