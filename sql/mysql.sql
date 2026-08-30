-- CREATE DATABASE IF NOT EXISTS talently;

CREATE TABLE users(
    full_name VARCHAR(100),
    yearly_salary INT,
    current_status ENUM("employed", "self-employed", "unemployed")
)