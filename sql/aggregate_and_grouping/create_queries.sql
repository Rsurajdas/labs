CREATE DATABASE restaurants;
CREATE TABLE payment_methods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200)
);
CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    num_seats INT,
    category VARCHAR(200)
);