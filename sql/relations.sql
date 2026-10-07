CREATE DATABASE relations;
CREATE TABLE cities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    -- id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE addresses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    -- id SERIAL PRIMARY KEY,
    house_name VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL,
    city_id INT,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    -- id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    address_id INT,
    FOREIGN KEY (address_id) REFERENCES addresses(id)
);
INSERT INTO cities (name)
VALUES ('Mumbai'),
    ('Pune'),
    ('Delhi'),
    ('Bengaluru'),
    ('Chennai'),
    ('Hyderabad'),
    ('Kolkata'),
    ('Jaipur'),
    ('Ahmedabad'),
    ('Lucknow');
INSERT INTO addresses (house_name, street, city_id)
VALUES ('Shanti Villa', 'MG Road', 1),
    ('Green Residency', 'FC Road', 2),
    ('Sunrise Apartments', 'Lajpat Nagar', 3),
    ('Lake View House', 'Indiranagar', 4),
    ('Ocean Heights', 'Anna Salai', 5),
    ('Sai Residency', 'Banjara Hills', 6),
    ('Rose Villa', 'Park Street', 7),
    ('Royal Enclave', 'MI Road', 8),
    ('Silver Heights', 'CG Road', 9),
    ('Ganga Residency', 'Hazratganj', 10);
INSERT INTO users (first_name, last_name, email, address_id)
VALUES ('Amit', 'Sharma', 'amit.sharma@example.com', 1),
    ('Priya', 'Patel', 'priya.patel@example.com', 2),
    ('Rahul', 'Verma', 'rahul.verma@example.com', 3),
    ('Sneha', 'Reddy', 'sneha.reddy@example.com', 4),
    ('Arjun', 'Kumar', 'arjun.kumar@example.com', 5),
    ('Neha', 'Singh', 'neha.singh@example.com', 6),
    ('Rohit', 'Das', 'rohit.das@example.com', 7),
    ('Pooja', 'Mehta', 'pooja.mehta@example.com', 8),
    ('Vikram', 'Joshi', 'vikram.joshi@example.com', 9),
    (
        'Anjali',
        'Gupta',
        'anjali.gupta@example.com',
        10
    );
SELECT u.id,
    first_name,
    last_name,
    email,
    house_name,
    street,
    c.name AS city_name
FROM users AS u
    INNER JOIN addresses AS a ON u.address_id = a.id
    INNER JOIN cities AS c ON a.city_id = c.id
WHERE c.id = 5
    OR c.id = 7
ORDER BY u.id DESC;
SELECT house_name,
    street,
    c.name AS city_name,
    first_name,
    last_name,
    email
FROM addresses AS a
    LEFT JOIN users AS u ON a.id = u.address_id
    LEFT JOIN cities AS c ON c.id = a.city_id;