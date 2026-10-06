-- CREATE DATABASE relations;
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