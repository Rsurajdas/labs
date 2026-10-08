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